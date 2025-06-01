from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="O‘zgartirilgan vaqt")

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    middle_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="O‘rta ism"
    )
    image = models.ImageField(
        upload_to='user_images/',
        null=True,
        blank=True,
        default='default.png',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
        verbose_name="Profil rasmi"
    )
    phone = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        verbose_name="Telefon raqam"
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['username']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})" if self.get_full_name() else self.username


class Role(BaseModel):
    role = models.CharField(
        max_length=200,
        verbose_name="Rol nomi"
    )
    description = models.TextField(
        verbose_name="Tavsif"
    )

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Rollar"
        ordering = ['role']

    def __str__(self):
        return self.role



class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name="Foydalanuvchi"
    )
    start_date = models.DateField(verbose_name="Ish boshlagan sana")
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ishdan ketgan sana"
    )
    about_skill = models.TextField(verbose_name="Ko'nikmalar haqida")
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Oylik maosh"
    )
    working_hours_per_week = models.FloatField(
        default=0,
        verbose_name="Haftalik ish soatlari"
    )

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"
        ordering = ['-start_date']

    def __str__(self):
        full_name = self.user.get_full_name()
        return f"{full_name if full_name else self.user.username}"


class UserRole(BaseModel):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name="Xodim"
    )
    role = models.ForeignKey(
        'Role',
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name="Rol"
    )

    class Meta:
        verbose_name = "Xodim roli"
        verbose_name_plural = "Xodim rollari"
        unique_together = ('employee', 'role')  # Har bir rol faqat bir marta biriktiriladi

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.role.role}"


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mijoz nomi")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    # company = models.CharField(max_length=255, blank=True, verbose_name="Kompaniya")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['name']

    def __str__(self):
        return self.name


class ClientInteraction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interactions', verbose_name="Mijoz")
    responsible = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Mas'ul operator"
    )
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mas'ul xodim")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Sana va vaqt")
    subject = models.CharField(max_length=255, verbose_name="Mavzu")
    notes = models.TextField(verbose_name="Xulosalar, izohlar")
    follow_up_date = models.DateTimeField(null=True, blank=True, verbose_name="Qayta aloqa sanasi")

    class Meta:
        verbose_name = "Aloqa"
        verbose_name_plural = "Aloqalar"
        ordering = ['-date']

    def __str__(self):
        return f"{self.client.name} - {self.subject} ({self.date.strftime('%Y-%m-%d %H:%M')})"