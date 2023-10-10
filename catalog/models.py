from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField()
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name="brands")
    importer = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="subs")
    name = models.CharField(max_length=256)
    color = models.CharField(max_length=256)
    icon = models.ImageField(null=True, blank=True)
    image = models.ImageField()
    cover = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sort = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('sort',)

    @property
    def product_count(self):
        count = self.products.count()
        return count

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, blank=True, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    name = models.CharField(max_length=256)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField()

    def __str__(self):
        return f'{self.product.name}'


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_discount = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.price}'


class FeaturedProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Seçilmiş Məhsul"
        verbose_name_plural = "Seçilmiş Məhsullar"

    def __str__(self):
        return self.product.name


class NewProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yeni Məhsul"
        verbose_name_plural = "Yeni Məhsullar"

    def __str__(self):
        return self.product.name
