from django.db import models
from django.urls import reverse
from accounts.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    contributer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    author = models.CharField(max_length=255)
    synopsis = models.TextField(blank=True)
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('bookclub:book_detail', args={self.pk})

    class Meta:
        ordering = ['-publication_year']
        verbose_name = 'book'
        verbose_name_plural = 'books'


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    anon_reviewer = models.CharField(max_length=255, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return self.title

    def reviewer_name(self):
        if self.user_reviewer:
            return self.user_reviewer.display_name
        return self.anon_reviewer or 'Anonymous'


class Bookmark(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_bookmarked = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'book')

    def __str__(self):
        return f'{self.profile} bookmarked {self.book}'


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, blank=True)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        return f'{self.book} borrowed'
