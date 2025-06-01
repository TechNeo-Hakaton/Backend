from django.db import models
from django.core.exceptions import ValidationError


class Location(models.Model):
    region = models.CharField(
        max_length=100,
        verbose_name="Viloyat (Region)"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Shahar (City)"
    )
    street = models.CharField(
        max_length=200,
        verbose_name="Ko‘cha (Street)"
    )
    destination = models.TextField(
        verbose_name="Mo‘ljal (Destination)"
    )

    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"
        ordering = ['region', 'city', 'street']

    def __str__(self):
        return f"{self.region}, {self.city}, {self.street}"


class Price(models.Model):
    rooms = models.PositiveIntegerField(
        verbose_name="Xonalar soni"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Narx (so‘m)"
    )

    class Meta:
        verbose_name = "Narx"
        verbose_name_plural = "Narxlar"
        ordering = ['rooms']

    def __str__(self):
        return f"{self.rooms} xonali — {self.price:,.2f} so‘m"


class Media(models.Model):
    description = models.TextField(
        verbose_name="Tavsif",
        blank=True
    )
    image = models.ImageField(
        upload_to='media/images/',
        null=True,
        blank=True,
        verbose_name="Rasm"
    )
    video = models.FileField(
        upload_to='media/videos/',
        null=True,
        blank=True,
        verbose_name="Video",
        help_text="MP4 format tavsiya etiladi"
    )

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media fayllar"
        ordering = ['-id']

    def __str__(self):
        return f"Media #{self.id}"

    def clean(self):
        # Faqat image yoki video kiritilgan bo'lishi kerak
        if not self.image and not self.video:
            raise ValidationError("Rasm yoki video fayllaridan kamida bittasi bo'lishi kerak.")
        if self.image and self.video:
            raise ValidationError("Faqat bittasini — rasm yoki videoni — yuklang.")


class Building(models.Model):
    image = models.ImageField(
        upload_to='building_images/',
        null=True,
        blank=True,
        verbose_name="Bino rasmi"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Bino nomi"
    )
    description = models.TextField(
        verbose_name="Tavsif"
    )
    location = models.ForeignKey(
        'Location',  # yoki boshqa tegishli model
        on_delete=models.CASCADE,
        verbose_name="Manzil"
    )
    budget = models.BigIntegerField(
        verbose_name="Byudjet (so‘m)"
    )
    start = models.DateField(
        verbose_name="Boshlanish sanasi"
    )
    end = models.DateField(
        verbose_name="Tugash sanasi"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Rejalashtirilgan'),
            ('in_progress', 'Jarayonda'),
            ('completed', 'Tugallangan'),
            ('canceled', 'Bekor qilingan'),
        ],
        default='pending',
        verbose_name="Holat"
    )

    class Meta:
        verbose_name = "Bino"
        verbose_name_plural = "Binolar"
        ordering = ['-start']

    def __str__(self):
        return self.name


class Flat(models.Model):
    project = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='flats',
        verbose_name="Bino (loyiha)"
    )
    floor = models.PositiveIntegerField(verbose_name="Qavat")
    rooms = models.PositiveIntegerField(verbose_name="Xonalar soni")
    price = models.BigIntegerField(verbose_name="Narx (so‘m)")
    area = models.FloatField(verbose_name="Maydoni (m²)")
    status = models.CharField(
        max_length=50,
        choices=[
            ('available', 'Bo‘sh'),
            ('sold', 'Sotilgan'),
            ('reserved', 'Band qilingan'),
        ],
        default='available',
        verbose_name="Holat"
    )
    has_balcony = models.BooleanField(default=False, verbose_name="Balkon mavjudmi")
    orientation = models.CharField(
        max_length=20,
        choices=[
            ('north', 'Shimol'),
            ('north_east', 'Shimol-Sharq'),
            ('east', 'Sharq'),
            ('south_east', 'Janub-Sharq'),
            ('south', 'Janub'),
            ('south_west', 'Janub-G‘arb'),
            ('west', 'G‘arb'),
            ('north_west', 'Shimol-G‘arb'),
        ],
        verbose_name="Yo‘nalish"
    )
    image = models.ImageField(
        upload_to='flats/images/',
        null=True,
        blank=True,
        verbose_name="Asosiy rasm"
    )

    class Meta:
        verbose_name = "Xonadon"
        verbose_name_plural = "Xonadonlar"
        ordering = ['project', 'floor', 'rooms']

    def __str__(self):
        return f"{self.project.name} - {self.floor}-qavat, {self.rooms} xonali"


class Material(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Material nomi"
    )
    unit = models.CharField(
        max_length=50,
        verbose_name="O‘lchov birligi"  # masalan: dona, kg, m³
    )
    count = models.PositiveIntegerField(
        verbose_name="Qoldiq soni"
    )
    total_count = models.PositiveIntegerField(
        verbose_name="Umumiy soni"
    )
    company = models.CharField(
        max_length=255,
        verbose_name="Yetkazib beruvchi"
    )
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name="Tegishli bino"
    )

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit})"
