from apps.categories.models import Category

TECH_CATEGORY, _ = Category.objects.get_or_create(
    name = "Tech",
    desc="Technology",
)

def assign_category(instance:any):
    category, _ = Category.objects.get_or_create(
        parent = TECH_CATEGORY,
        name = instance.spec,
        desc = f'All {instance.spec}\'s must use this category'
    )
    instance.product.categories.add(category)
    instance.product.save()