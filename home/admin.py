from django.contrib import admin
from . models import *
# Register your models here.

class SettingAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'company','icon','logo','menu_icon','cart_icon','about_img')
    list_display_links = ['id','title', 'company' ]
    
   
class ContactMessageAdmin(admin.ModelAdmin):
    list_display=('name','email','phone', 'subject','message','status', 'note')
    readonly_fields = ('name', 'subject','email', 'message')
    list_filter= ['status']
    list_display_links = ('status','name','note')
    search_fields = ('name','email', 'subject','message','status', 'note')
    list_per_page = 20

    
class BrandAdmin(admin.ModelAdmin):
    list_display= ['id','brands']

class BannerAdmin(admin.ModelAdmin):
    list_display= ['id','image']

class SampleAdmin(admin.ModelAdmin):
    list_display= ['id','image','title']

class TrainingAdmin(admin.ModelAdmin):
    list_display= ['id','image','title','heading','fee','link']


class  CategoryAdmin(admin.ModelAdmin):
    list_display= ['id','title','image' ]
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display= ['id','title', 'category','image','maxquantity','available','slug']
    list_filter= ['category']
    list_display_links = ('title', 'category','image')
    readonly_fields= ('image_tag',)
    prepopulated_fields = {'slug': ('title',)}
    

class ShopCartAdmin(admin.ModelAdmin):
    list_display=('order_code','user', 'product', 'quantity','price', 'amount','order_placed')
    list_filter= ['user']
    list_display_links = ['product']
    readonly_fields = ('order_code','user', 'product', 'quantity','price', 'amount','order_placed')
    can_delete = False



class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('order_code','user','order_placed','payment_code','total','status','created','updated')
    list_filter = ['status']
    list_display_links = ['user']
    readonly_fields = ('order_code','user','order_placed','payment_code','total','status','created','updated')
    can_delete = False
      

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username','first_name', 'last_name','image','email', 'address', 'phone', 'city', 'country']



class TrainingRegAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','fee', 'phone', 'pay_date', 'start_date','started', 'end_date','ended']
    list_editable = ['start_date', 'started']

    
admin.site.index_title = 'Floles Organics Admin Site'   # default: "Site administration"
admin.site.site_title = 'Floles Admin'    # default: "Django site admin"
# admin.site.site_header = "Floles Organics"   default: "Django Administration"
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TrainingReg, TrainingRegAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(ShopCart, ShopCartAdmin)  
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Setting, SettingAdmin)  
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Training, TrainingAdmin)
   
