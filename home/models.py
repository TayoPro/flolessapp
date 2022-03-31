from django.db import models
from datetime import date
from django.forms import ModelForm
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe



# Create your models here.
class Setting(models.Model):
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=50, null=True)
    address = models.CharField( max_length=100)
    phone = models.CharField( null=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    icon = models.ImageField(blank=True,null=True,  upload_to='images/',default='picture.jpg')
    logo = models.ImageField(blank=True,null=True, upload_to='images/',default='picture.jpg')
    cart_icon = models.ImageField(blank=True,null=True, upload_to='images/',default='picture.jpg')
    menu_icon = models.ImageField(blank=True,null=True, upload_to='images/',default='picture.jpg')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    about =RichTextUploadingField(blank=True)
    about2 =RichTextUploadingField(blank=True)
    about_img = models.ImageField(blank=True,null=True, upload_to='about/',default='picture.jpg')
    contact =RichTextUploadingField(blank=True)
    
    def __str__(self):
        return self.title


class Banner(models.Model):
    image = models.ImageField(blank=True,null=True, upload_to='banner/',default='picture.jpg')    

    
class Brand(models.Model):
    brands = models.ImageField(blank=True,null=True, upload_to='brand/',default='picture.jpg')    


class Sample(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(blank=True,null=True, upload_to='samples/',default='picture.jpg')    

    def __str__(self):
        return self.title

 
class ContactMessage(models.Model):
    STATUS =(
        ('New', 'New'),
        ('Read', 'Read'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    )

    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=20)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    note = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model= ContactMessage
        fields = ['name', 'email','phone', 'subject', 'message']


class Category(models.Model):
    STATUS =(
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    image = models.ImageField(blank=True, upload_to='images/',default='picture.jpg')
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    AVAILABLE =(
        ('In Stock', 'In Stock'),
        ('Out Of Stock', 'Out Of Stock'),
        ('ReStocked', 'ReStocked'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(null=False, unique=True)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image= models.ImageField(blank=True,null=True, upload_to='images/', default='picture.jpg')
    price = models.FloatField(null=True, blank=True)
    discount= models.FloatField(blank=True, null=True)
    available= models.CharField(choices=AVAILABLE, max_length=15, default='In Stock')
    maxquantity = models.IntegerField(null=True, blank=True)
    minquantity = models.IntegerField(blank=True)
    amount = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    glow = models.BooleanField(blank=True)
    whitening = models.BooleanField(blank=True)
    lightening = models.BooleanField(blank=True)
    detail = RichTextUploadingField()
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug}) 



class Training(models.Model):
    title = models.CharField(max_length=250)
    heading = models.CharField(max_length=250)
    fee = models.FloatField(null=True, blank=True, default=5000)
    image = models.ImageField(blank=True, upload_to='training/',default='picture.jpg')
    detail = RichTextUploadingField()
    link = models.CharField(max_length=250, blank=True, null=True)


    def __str__(self):
        return self.title



class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(blank=True ,null=False)
    order_code = models.CharField(max_length=70, editable=False)
    order_placed = models.BooleanField(default=False)

    def __str__(self):        
        return self.product.title
     

    @property
    def price(self):
        if self.product_id is not None:
            return (self.product.price)


    @property
    def amount(self):
        if self.product_id is None:
            return(None)
        else:                
            if self.product.discount:
                return(self.product.discount * self.quantity)
            else:
                return(self.product.price * self.quantity)
                   

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
       
      


class Checkout(models.Model):
    STATUS =(
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total = models.FloatField(null=True, blank=True)
    order_placed = models.BooleanField(default=False)
    order_code = models.CharField(max_length=70, editable=False)
    payment_code = models.CharField(max_length=8, editable=False)
    first_name = models.CharField(max_length=15)
    last_name= models.CharField(max_length=15)
    phone= models.CharField(blank=True, null=True, max_length=20)
    address = models.CharField(max_length=150,  null=True,blank=True)
    city = models.CharField(blank=True, null=True, max_length=20)
    state = models.CharField(blank=True, null=True, max_length=20)
    country = models.CharField(blank=True, null=True, max_length=20)
    status = models.CharField(max_length=10, null=True, choices=STATUS, default='New')
    adminnote = models.CharField(blank=True, null=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
       
    
    def __str__(self):
        return self.user.username



class OrderForm(ModelForm):
    class Meta:
        model = Checkout
        fields = ['first_name', 'last_name', 'address', 'phone', 'city', 'country']



class UserProfile(models.Model):
    user = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(blank=True, max_length=20, null= True)
    last_name = models.CharField(blank=True, max_length=20, null= True)
    phone = models.CharField(blank=True,null=True, max_length=15)
    address = models.CharField(blank=True,null=True, max_length=150)
    city = models.CharField(blank=True,null=True, max_length=20)
    state = models.CharField(blank=True,null=True, max_length=20)
    country = models.CharField(blank=True,null=True, max_length=50)
    zipcode = models.CharField(blank=True,null=True, max_length=8)
    image = models.ImageField(blank=True, null=True, upload_to='profile', default='avatar2.jpg')

    def __str__(self):              
        return self.user.username


    @property
    def username(self):
        if self.user_id is not None:
            return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] ' 


    @property
    def email(self):
      if self.user_id is not None:
        return (self.user.email)

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'
    
    class Meta:
        db_table = 'userprofile' 
        managed = True
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'





class TrainingReg(models.Model):
    user = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(blank=True, max_length=20, null= True)
    last_name = models.CharField(blank=True, max_length=20, null= True)
    phone = models.CharField(blank=True, max_length=15)
    fee = models.FloatField(null=True, blank=True, editable=False)
    payment_code = models.CharField(blank=True, max_length=8)
    email = models.EmailField()
    paid = models.BooleanField(default=False)
    pay_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    started = models.BooleanField(default=False)
    end_date = models.DateTimeField(auto_now=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    @property
    def username(self):
        if self.user_id is not None:
            return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] ' 


    @property
    def email(self):
      if self.user_id is not None:
        return (self.user.email)

        
    class Meta:
        db_table = 'TrainingReg' 
        managed = True
        verbose_name = 'TrainingReg'
        verbose_name_plural = 'TrainingReg'



