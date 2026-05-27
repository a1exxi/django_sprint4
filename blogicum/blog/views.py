from django.contrib.auth import get_user_model           # получаем модель пользователя
from django.contrib.auth.forms import UserCreationForm    # стандартная форма регистрации
from django.shortcuts import redirect                    # перенаправление на другую страницу
from django.shortcuts import render, get_object_or_404   # render — рендер шаблона, get_object_or_404 — найти или 404
from django.utils import timezone                        # работа с датой и временем
from django.core.paginator import Paginator              # разбивка списка на страницы (пагинация)
from django.contrib.auth.decorators import login_required  # декоратор — требует авторизации
from django.db.models import Count, Q                    # Count — подсчёт (например, комментариев), Q — сложные фильтры
from django.http import Http404                          # исключение "страница не найдена"


from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, ProfileEditForm

# get_user_model() — достаём модель пользователя, которая используется в проекте
User = get_user_model()


def index(request):
    """Главная страница: список последних опубликованных постов."""
    # select_related — подгружает связанные объекты (автора, локацию, категорию) одним запросом,
    # чтобы не делать лишних обращений к базе.
    posts_qs = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        # Q — позволяет делать сложные условия.
        # Показываем посты: либо без привязки к локации, либо с опубликованной локацией.
        Q(location__isnull=True) | Q(location__is_published=True),
        is_published=True,                   # только опубликованные
        pub_date__lte=timezone.now(),        # дата публикации не позже текущего момента (__lte = меньше или равно)
        category__is_published=True,         # категория поста опубликована
    ).annotate(
        comment_count=Count('comments')      # добавляем к каждому посту количество комментариев
    ).order_by('-pub_date')                  # сортируем: сначала новые

    # Paginator — разбивка на страницы (10 постов на странице)
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')    # читаем номер страницы из URL (?page=2)
    page_obj = paginator.get_page(page_number)  # получаем объекты для текущей страницы

    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    """Страница одного поста."""
    # get_object_or_404 — ищем пост по id; если не нашли — вернётся страница 404
    post = get_object_or_404(Post.objects.select_related('author', 'category', 'location'), id=post_id)

    # Если зашёл не автор поста (или аноним) — проверяем, что пост вообще должен быть виден
    if (not request.user.is_authenticated) or (request.user.pk != post.author_id):
        if not post.is_published:
            raise Http404                # скрытый пост — 404
        if post.pub_date > timezone.now():
            raise Http404                # пост с будущей датой — 404
        if not post.category.is_published:
            raise Http404                # скрытая категория — 404
        if post.location and not post.location.is_published:
            raise Http404                # скрытая локация — 404

    # Все комментарии к этому посту
    comments = post.comments.select_related('author').all()
    form = CommentForm()                # пустая форма для нового комментария
    template = 'blog/detail.html'
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Страница с постами выбранной категории."""
    # Ищем категорию по slug; только если опубликована
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts_qs = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        Q(location__isnull=True) | Q(location__is_published=True),
        category=category,               # отфильтровали по категории
        is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_obj,
    })


def registration(request):
    """Регистрация нового пользователя."""
    # UserCreationForm — стандартная форма Django для регистрации
    # request.POST or None — если пришёл POST, берём данные из него, иначе создаём пустую форму
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()                                  # сохраняем нового пользователя
        return redirect('blog:profile', username=user.username)  # переходим на его страницу профиля
    return render(request, 'registration/registration_form.html', {'form': form})


def profile(request, username):
    """Страница профиля пользователя со списком его постов."""
    profile_user = get_object_or_404(User, username=username)

    # Берём все посты автора
    posts_qs = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        author=profile_user
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    # Если это чужой профиль — показываем только опубликованные посты
    if request.user != profile_user:
        posts_qs = posts_qs.filter(
            Q(location__isnull=True) | Q(location__is_published=True),
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/profile.html', {
        'profile': profile_user,
        'page_obj': page_obj,
    })


# @login_required — декоратор: если пользователь не залогинен, его перенаправит на страницу входа
@login_required
def post_create(request):
    """Создание нового поста."""
    # request.FILES — файлы, загруженные через форму (например, картинка)
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)      # commit=False — не сохраняем в базу, пока не заполним автора
        post.author = request.user          # ставим автором текущего пользователя
        post.save()                         # теперь сохраняем
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Редактирование существующего поста."""
    post = get_object_or_404(Post, id=post_id)

    # Если редактор — не автор, перенаправляем на страницу поста (или на главную)
    if request.user != post.author:
        is_public = (
            post.is_published
            and post.pub_date <= timezone.now()
            and post.category.is_published
            and (post.location is None or post.location.is_published)
        )
        if is_public:
            return redirect('blog:post_detail', post_id=post.id)
        return redirect('blog:index')

    # Передаём instance=post, чтобы форма была заполнена текущими данными поста
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return post_detail(request, post_id=post.id)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def post_delete(request, post_id):
    """Удаление поста."""
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)

    form = PostForm(instance=post)

    if request.method == 'POST':
        post.delete()                                 # удаляем из базы
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    """Добавление комментария к посту."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)             # не сохраняем — сначала заполняем автора и пост
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'comment': comment})


@login_required
def edit_profile(request):
    """Редактирование профиля текущего пользователя."""
    # instance=request.user — форма будет заполнена данными текущего пользователя
    form = ProfileEditForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/user.html', {'form': form})