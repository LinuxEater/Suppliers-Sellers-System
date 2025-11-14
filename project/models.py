from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
import uuid


def product_image_upload_to(instance, filename):
    product_id = instance.product.id if instance and instance.product_id else 'unassigned'
    return f'products/{product_id}/images/{uuid.uuid4()}_{filename}'


def product_video_upload_to(instance, filename):
    product_id = instance.id if instance and instance.id else 'unassigned'
    return f'products/{product_id}/video/{uuid.uuid4()}_{filename}'


def vendor_profile_image_upload_to(instance, filename):
    return f'vendors/{instance.id}/profile_image/{uuid.uuid4()}_{filename}'


class Supplier(models.Model):
    name = models.CharField('nome', max_length=200)
    contact_email = models.EmailField('e-mail', blank=True, null=True)
    contact_phone = models.CharField('telefone', max_length=30, blank=True)
    document = models.CharField('documento (CNPJ/CPF)', max_length=40, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.name


class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile', null=True, blank=True)
    name = models.CharField('nome', max_length=200)
    phone = models.CharField('telefone', max_length=30, blank=True)
    profile_image = models.ImageField('imagem de perfil', upload_to=vendor_profile_image_upload_to, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

    def __str__(self):
        return self.name


class PlatformFeeConfig(models.Model):
    cost_fixed = models.DecimalField('Custo Fixo', max_digits=8, decimal_places=2, default=Decimal('0.00'))
    physical_margin = models.DecimalField('Margem Física Padrão (%)', max_digits=5, decimal_places=2, default=Decimal('30.00'))
    shopee_commission = models.DecimalField('Comissão Shopee (%)', max_digits=5, decimal_places=2, default=Decimal('14.00'))
    free_shipping_fee = models.DecimalField('Programa Frete Grátis (%)', max_digits=5, decimal_places=2, default=Decimal('6.00'))
    fixed_fee = models.DecimalField('Taxa Fixa (R$)', max_digits=8, decimal_places=2, default=Decimal('4.00'))
    highlight_active = models.BooleanField('Campanha Destaque Ativa?', default=True)
    highlight_fee = models.DecimalField('Taxa Campanha Destaque (%)', max_digits=5, decimal_places=2, default=Decimal('3.00'))

    class Meta:
        verbose_name = 'Configuração de Taxas'
        verbose_name_plural = 'Configurações de Taxas'

    def __str__(self):
        return 'Configuração Padrão de Taxas'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_code = models.CharField('código do produto', max_length=60, unique=True)
    name = models.CharField('nome', max_length=255)
    description = models.TextField('descrição', blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    cost_price = models.DecimalField('preço de custo', max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0)
    recommended_price = models.DecimalField('preço recomendado', max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    negotiation_margin = models.DecimalField('margem de negociação (%)', max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))])

    stock = models.IntegerField('estoque', default=0)
    is_active = models.BooleanField('ativo', default=True)

    video_file = models.FileField('vídeo (opcional)', upload_to=product_video_upload_to, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'webm', 'mkv'])])

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product_code} — {self.name}"

    def clean(self):
        super().clean()
        if self.video_file and hasattr(self.video_file, 'size'):
            max_mb = 50
            if self.video_file.size > max_mb * 1024 * 1024:
                raise ValidationError({'video_file': f'Vídeo muito grande. Máximo {max_mb} MB.'})

    @property
    def min_price_allowed(self):
        if self.recommended_price is None:
            return None
        margin_fraction = (self.negotiation_margin / Decimal('100'))
        min_price = (self.recommended_price * (Decimal('1.00') - margin_fraction)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        return min_price

    @property
    def vf_fisica(self):
        config = PlatformFeeConfig.objects.first()
        if not config:
            return None
        custo_total = self.cost_price + config.cost_fixed
        vf_fisica = custo_total * (1 + config.physical_margin / 100)
        return vf_fisica.quantize(Decimal('0.01'))

    @property
    def vf_shopee(self):
        config = PlatformFeeConfig.objects.first()
        if not config:
            return None
        custo_total = self.cost_price + config.cost_fixed
        taxa_total = config.shopee_commission + config.free_shipping_fee + (config.highlight_fee if config.highlight_active else Decimal('0.00'))
        vf_shopee = (custo_total + config.fixed_fee) * (1 + taxa_total / 100)
        return vf_shopee.quantize(Decimal('0.01'))

    def images_count(self):
        return self.images.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('imagem', upload_to=product_image_upload_to, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    alt_text = models.CharField('texto alternativo', max_length=255, blank=True)
    position = models.PositiveSmallIntegerField('posição', default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Imagem do produto'
        verbose_name_plural = 'Imagens dos produtos'
        ordering = ['position', 'created_at']
        unique_together = (('product', 'position'),)

    def __str__(self):
        return f"Imagem {self.position} de {self.product.product_code}"

    def clean(self):
        super().clean()
        if self.product_id:
            existing = ProductImage.objects.filter(product_id=self.product_id)
            if not self.pk and existing.count() >= 5:
                raise ValidationError('Não é possível enviar mais de 5 imagens por produto.')
            if self.image and hasattr(self.image, 'size'):
                max_mb = 5
                if self.image.size > max_mb * 1024 * 1024:
                    raise ValidationError({'image': f'Imagem muito grande. Máximo {max_mb} MB.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=ProductImage)
def ensure_image_position(sender, instance, **kwargs):
    if instance.product_id and (instance.position is None or instance.position < 0):
        instance.position = 0
    if instance.product_id and instance.position >= 5:
        raise ValidationError('A posição da imagem deve estar entre 0 e 4.')
    if instance.product_id and not instance.pk:
        occupied = set(ProductImage.objects.filter(product=instance.product).values_list('position', flat=True))
        if instance.position in occupied:
            for i in range(5):
                if i not in occupied:
                    instance.position = i
                    break


class Sale(models.Model):
    PLATFORM_CHOICES = [
        ('loja_fisica', 'Loja Física'),
        ('shopee', 'Shopee'),
        ('outros', 'Outros'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name='Produto')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales', verbose_name='Vendedor')
    quantity = models.PositiveIntegerField('Quantidade Vendida', default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField('Preço Total da Venda', max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    platform = models.CharField('Plataforma de Venda', max_length=20, choices=PLATFORM_CHOICES, default='loja_fisica')
    sale_date = models.DateTimeField('Data da Venda', default=timezone.now)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-sale_date']

    def __str__(self):
        return f'Venda de {self.quantity}x {self.product.name} em {self.sale_date.strftime("%d/%m/%Y")}'


class StockHistory(models.Model):
    REASON_CHOICES = [
        ('new_stock', 'Novo Estoque'),
        ('sale', 'Venda'),
        ('manual_adjustment', 'Ajuste Manual'),
        ('initial_stock', 'Estoque Inicial'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_history')
    change = models.IntegerField('Alteração no Estoque')
    reason = models.CharField('Motivo', max_length=20, choices=REASON_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico de Estoque'
        verbose_name_plural = 'Históricos de Estoque'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.product.name}: {self.change} em {self.timestamp.strftime("%d/%m/%Y")}'


from django.db.models.signals import post_save
from .utils import send_low_stock_notification

@receiver(post_save, sender=Sale)
def record_sale_in_stock_history(sender, instance, created, **kwargs):
    if created:
        StockHistory.objects.create(
            product=instance.product,
            change=-instance.quantity,
            reason='sale'
        )
        # Update product stock
        product = instance.product
        product.stock -= instance.quantity
        product.save(update_fields=['stock'])

        # Check for low stock
        if product.stock < settings.LOW_STOCK_THRESHOLD:
            send_low_stock_notification(product)


@receiver(pre_save, sender=Product)
def record_manual_stock_adjustment(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            if old_instance.stock != instance.stock:
                change = instance.stock - old_instance.stock
                reason = 'manual_adjustment' # Corrected line
                if change != 0:
                    StockHistory.objects.create(
                        product=instance,
                        change=change,
                        reason=reason
                    )
                    # Check for low stock after manual adjustment
                    if instance.stock < settings.LOW_STOCK_THRESHOLD:
                        send_low_stock_notification(instance)
        except Product.DoesNotExist:
            pass # New product, initial stock will be handled separately if needed
    else:
        # This is a new product, we can create an initial stock record
        if instance.stock > 0:
            # This will be created after the product is saved, so we need a post_save signal for new products
            pass

@receiver(post_save, sender=Product)
def record_initial_stock(sender, instance, created, **kwargs):
    if created and instance.stock > 0:
        StockHistory.objects.create(
            product=instance,
            change=instance.stock,
            reason='initial_stock'
        )