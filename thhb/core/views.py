from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from .models import BlogPost
from django.shortcuts import redirect

import os


@login_required(login_url='/under_construction/')
def home(request):
    post = BlogPost.objects.latest('pub_date')
    return render(request, 'index.html', {'post': post})


@login_required(login_url='/under_construction/')
def book(request):
    return render(request, 'thebook.html')


def no_access_view(request):
    return render(request, 'under_construction.html')


@login_required(login_url='/under_construction/')
def userpage(request):
    return render(request, 'userpage.html')


def get_word_count(str_var):
    """
    The blog posts, entered via TinyMCE, have HTML in them. To get a more accurate word count,
    we first remove much of the HTML (etc.) that commonly comes from a rich text editor.
    """
    ret_str = str_var.replace("<p class='parag'>", "") \
                     .replace("</p>", "") \
                     .replace("<em>", "") \
                     .replace("</em>", "") \
                     .replace("\n", "") \
                     .replace("&ndash;", "") \
                     .replace("&rsquo;", "") \
                     .replace("&lsquo;", "") \
                     .replace("&ldquo;", "") \
                     .replace("&rdquo;", "") \
                     .replace("<a href=", "") \
                     .replace("<span style=", "")

    return len(ret_str.split())


@login_required(login_url='/under_construction/')
def show_single_post(request, post_slug):
    blog_post = BlogPost.objects.get(slug=post_slug)
    if post_slug == 'the-book':
        """
        # Because the template thebook.html is laid out a bit differently than other
        # posts, the content is split into two paragraphs that go before the
        # picture, and those that come after it
        """
        chunks = blog_post.content.replace('\n', '').split('</p>')
        first_paragraphs, last_paragraphs = '</p>'.join(chunks[:2]) + '</p>', '</p>'.join(chunks[2:])
        return render(request, 'thebook.html', {'blog_post': blog_post,
                                                'first_paragraphs': first_paragraphs,
                                                'last_paragraphs': last_paragraphs})

    word_count = get_word_count(blog_post.content)
    return render(request, 'single_post.html', { 'blog_post': blog_post, 'word_count': word_count })


@login_required(login_url='/under_construction/')
def post_list(request):
    posts = BlogPost.objects.filter(category='MN')
    return render(request, 'post_list.html', {'posts': posts})


def adjust_content(content):
    """
    The TinyMCE text editor returns its own HTML, which needs to be adjusted a bit to remove
    superfluous material and add the appropriate class to paragraphs...
    """
    new_content = content.replace('<p>&nbsp;</p>', '') \
                     .replace('\r', '') \
                     .replace('<p>', "<p class='parag'>") \
                     .replace('<p lang="en-GB">', "<p class='parag'>") \
                     .replace('<p lang="en-CA">', "<p class='parag'>") \
                     .replace('<p lang="en-US">', "<p class='parag'>") \
                     .replace('<span lang="en-GB">', '') \
                     .replace('<span lang="en-CA">', '') \
                     .replace('<span lang="en-US">', '') \
                     .replace('</span>', '')
#                     .replace('<a', '<a target="_blank" rel="noopener noreferrer"')

    return new_content


@login_required(login_url='/under_construction/')
def create_blogpost(request):
    if request.user.write_access:
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.content = adjust_content(new_post.content)
                new_post.save()
                return redirect(f'/{new_post.slug}/')
            else:
                print("Form not valid. Errors: {form.errors}")
        else:
            form = BlogPostForm()

        return render(request, 'blogpost.html', { 'form':form })
    else:
        return render(request, 'insufficient_privileges.html')


@login_required(login_url='/under_construction/')
def update_blogpost(request, post_slug):
    blog_post = get_object_or_404(BlogPost, slug = post_slug)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance = blog_post)

    if request.user.write_access:
        if request.method == 'POST':
            old_version = BlogPost.objects.get(slug = post_slug)
            if form.is_valid():
                # The old version of the image must be deleted
                image_path = old_version.image.url
                if image_path[0] == '/': # If the path starts out with '/static', it doesn't get found
                    image_path = image_path[1:]
                if os.path.exists(image_path):
                    os.remove(image_path)

                updated_post = form.save(commit=False)
                updated_post.content = adjust_content(updated_post.content)
                updated_post.save()
                return redirect(f'/{updated_post.slug}/')
        else:
            context = {'form': form}
            return render(request, 'blogpost.html', context)
    else:
        return render(request, 'insufficient_privileges.html')