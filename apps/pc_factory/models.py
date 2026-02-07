from django.db import models
from apps.items.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.categories.models import Category
from .utils import assign_category

color_choices = [
        ("BL", "Black"),
        ("WH", "White"),
    ]



class MotherboardSpecs(models.Model):
    spec = "Motherboard"
    
    socket_choices = [
        ("AM4", "AM4"),
        ("AM5", "AM5"),
        ("LGA12", "LGA1200"),
        ("LGA1700", "LGA1700"),
    ]

    form_factor_choices = [
        ("ATX", "STANDARD-ATX"),
        ("MCATX", "MICRO-ATX"),
        ("MNATX", "MINI-ATX"),
        ("NNATX", "NANO-ATX"),
    ]

    memory_type_choices = [
        ("D4", "DDR4"),
        ("D5", "DDR5"),
    ]

    memory_channels_choices = [
        ("SC", "SINGLE-CHANNEL"),
        ("DC", "DUAL-CHANNEL"),
    ]


    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="motherboard_specs")
    chipset = models.CharField(max_length=50, blank=True, null=True)
    socket = models.CharField(max_length=20, blank=True, null=True, choices=socket_choices)
    form_factor = models.CharField(max_length=20, blank=True, null=True, choices=form_factor_choices)
    memory_channels = models.CharField(max_length=20, default="DC", choices=memory_channels_choices)
    max_memory = models.PositiveSmallIntegerField(blank=True, null=True)  # In GB
    memory_slots = models.PositiveSmallIntegerField(blank=True, null=True)
    memory_type = models.CharField(max_length=20, blank=True, null=True, choices=memory_type_choices)  # DDR4, DDR5, etc.
    pci_express_slots = models.PositiveSmallIntegerField(blank=True, null=True)
    m2_slots = models.PositiveSmallIntegerField(blank=True, null=True)
    sata_ports = models.PositiveSmallIntegerField(blank=True, null=True)
    usb_ports = models.PositiveSmallIntegerField(blank=True, null=True)
    wifi = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    rgb_lighting = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    class Meta:
        verbose_name = "Motherboard Specification"
        verbose_name_plural = "Motherboard Specifications"

    def __str__(self):
        return f"{self.product.name}"

class CPUSpecs(models.Model):
    spec = "CPU"

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="cpu_specs")
    cores = models.PositiveIntegerField(null=True, blank=True)
    threads = models.PositiveIntegerField(null=True, blank=True)
    base_clock = models.FloatField(null=True, blank=True)
    boost_clock = models.FloatField(null=True, blank=True)
    tdp = models.PositiveIntegerField(null=True, blank=True)  # Thermal Design Power in watts

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name = "CPU Spec"
        verbose_name_plural = "CPU Specs"

class GPUSpecs(models.Model):
    spec = "GPU"


    memory_type_choices = [
        ("G6","GDDR6"),
        ("G7","GDDR7"),
    ]

    bus_interface_choices = [
        ("E4X16", "PCIe 4.0 x16"),
        ("E5X16", "PCIe 5.0 x16"),
    ]

    

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="gpu_specs")
    vram = models.PositiveIntegerField(null=True, blank=True)
    base_clock = models.FloatField(null=True, blank=True)
    boost_clock = models.FloatField(null=True, blank=True)
    memory_clock = models.FloatField(null=True, blank=True)
    memory_type = models.CharField(max_length=20, null=True, blank=True, choices=memory_type_choices)
    memory_bus = models.PositiveIntegerField(null=True, blank=True)
    bus_interface = models.CharField(max_length=40, null=True, blank=True, choices=bus_interface_choices)
    power_consumption = models.PositiveIntegerField(null=True, blank=True)
    color = models.CharField(max_length=20, default="BL", choices=color_choices)

    def save(self, *args, **kwargs):
        assign_category(instance=self)


        super().save(args, kwargs)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name = "GPU Spec"
        verbose_name_plural = "GPU Specs"

class RAMSpecs(models.Model):
    spec = "RAM"
    type_choices = (
        ("DDR4", "DDR4"),
        ("DDR5", "DDR5"),
    )
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="ram_specs")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True, choices=type_choices)
    speed = models.PositiveIntegerField(null=True, blank=True)
    color = models.CharField(max_length=20, default="BL", choices=color_choices)
    rgb = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name = "RAM Spec"
        verbose_name_plural = "RAM Specs"

class PSUSpecs(models.Model):
    spec = "PSU"


    PRODUCT_TYPE_CHOICES = [
        ('80+', '80 Plus'),
        ('80_Bronze', '80 Plus Bronze'),
        ('80_Silver', '80 Plus Silver'),
        ('80_Gold', '80 Plus Gold'),
        ('80_Platinum', '80 Plus Platinum'),
        ('80_Titanium', '80 Plus Titanium'),
    ]
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="psu_specs")
    wattage = models.PositiveIntegerField(null=True, blank=True)  # Wattage of PSU
    efficiency = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES, null=True, blank=True)  # Efficiency rating
    color = models.CharField(max_length=20, default="BL", choices=color_choices)

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name = "PSU Spec"
        verbose_name_plural = "PSU Specs"

class CaseSpecs(models.Model):
    spec = "Case"

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="case_specs")
    form_factor = models.CharField(max_length=50, choices=[
        ("Mid Tower", "Mid Tower"),
        ("Full Tower", "Full Tower"),
        ("Mini Tower", "Mini Tower"),
        ("ITX", "ITX")
    ])
    motherboard_support = models.CharField(max_length=100, help_text="Compatible motherboard sizes")
    material = models.CharField(max_length=100, help_text="Materials used in the case")
    fan_support = models.CharField(max_length=255, help_text="Number and placement of supported fans")
    radiator_support = models.CharField(max_length=255, help_text="Maximum supported radiator sizes")
    gpu_clearance = models.PositiveSmallIntegerField(help_text="Maximum GPU length in mm")
    cpu_cooler_clearance = models.PositiveSmallIntegerField(help_text="Maximum CPU cooler height in mm")
    psu_clearance = models.PositiveSmallIntegerField(help_text="Maximum PSU length in mm")
    rgb_lighting = models.BooleanField(default=False, help_text="Does the case have built-in RGB lighting?")
    front_panel_io = models.TextField(help_text="List of front panel ports and buttons")
    dimensions = models.CharField(max_length=50, help_text="Case dimensions (WxDxH)")
    weight = models.FloatField(help_text="Weight of the case in kg")
    color = models.CharField(max_length=20, default="BL", choices=color_choices)

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    class Meta:
        verbose_name = "Case Specification"
        verbose_name_plural = "Case Specifications"

    def __str__(self):
        return f"{self.product.name}"

class StorageSpecs(models.Model):
    spec = "Storage"

    SSD = 'SSD'
    HDD = 'HDD'
    NVME = 'NVMe'
    
    STORAGE_TYPE_CHOICES = [
        (SSD, 'SSD'),
        (HDD, 'HDD'),
        (NVME, 'NVMe'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="storage_specs")
    capacity = models.PositiveIntegerField(null=True, blank=True)  # Storage capacity in GB
    type = models.CharField(max_length=50, null=True, blank=True, choices=STORAGE_TYPE_CHOICES)  # SSD, HDD, NVMe
    read_speed = models.PositiveIntegerField(null=True, blank=True)  # Read speed in MB/s
    write_speed = models.PositiveIntegerField(null=True, blank=True)  # Write speed in MB/s

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        self.product.categories
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name = "Storage Spec"
        verbose_name_plural = "Storage Specs"

class CoolerSpecs(models.Model):
    spec = "Cooler"

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="cooler_specs")
    type = models.CharField(max_length=50, choices=[("Air Cooler", "Air Cooler"), ("Liquid Cooler", "Liquid Cooler")])
    fan_size = models.PositiveSmallIntegerField(help_text="Size of the fan in mm")
    max_rpm = models.PositiveSmallIntegerField(help_text="Maximum RPM of the fan")
    noise_level = models.CharField(max_length=20, help_text="Noise level in dBA")
    tdp_rating = models.PositiveSmallIntegerField(help_text="Maximum TDP supported (in Watts)")
    compatibility = models.TextField(help_text="Supported CPU sockets (Intel/AMD)")
    rgb_lighting = models.BooleanField(default=False, help_text="Does the cooler have RGB lighting?")
    dimensions = models.CharField(max_length=50, help_text="Dimensions of the cooler (WxDxH)")
    weight = models.PositiveSmallIntegerField(help_text="Weight in grams")
    color = models.CharField(max_length=20, default="BL", choices=color_choices)

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    class Meta:
        verbose_name = "Cooler Specification"
        verbose_name_plural = "Cooler Specifications"

    def __str__(self):
        return f"{self.product.name}"

class NetworkingSpecs(models.Model):
    spec = "Networking"

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="networking_specs")
    ports = models.CharField(max_length=255, null=True, blank=True)  # e.g., Ethernet, Wi-Fi
    speed = models.PositiveIntegerField(null=True, blank=True)  # Speed in Mbps

    def save(self, *args, **kwargs):
        assign_category(instance=self)
        super().save(args, kwargs)

    def __str__(self):
        return f"Networking Specs for {self.product.name}"

    class Meta:
        verbose_name = "Networking Spec"
        verbose_name_plural = "Networking Specs"


class PC(models.Model):
    spec = "PC"

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="PC_specs")
    motherboard = models.ForeignKey(MotherboardSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    cpu = models.ForeignKey(CPUSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    gpu = models.ForeignKey(GPUSpecs, on_delete=models.SET_NULL, null=True, blank=True)
    ram = models.ForeignKey(RAMSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    ram_quantity = models.IntegerField(validators=[MaxValueValidator(4, "You can stack up to 4 ram sticks")], default=1, null=False, blank=False)
    storage = models.ForeignKey(StorageSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    case = models.ForeignKey(CaseSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    psu = models.ForeignKey(PSUSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    cooling = models.ForeignKey(CoolerSpecs, on_delete=models.SET_NULL, null=True, blank=False)
    networking = models.ForeignKey(NetworkingSpecs, on_delete=models.SET_NULL, null=True, blank=True)
    aesthetics = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the aesthetics of the PC (1 to 5)",
        null=True
    )
    performance = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the performance of the PC (1 to 5)",
        null=True
    )
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the pricing fairness/value (1 to 5)",
        null=True
    )

    def save(self, *args, **kwargs):

        final_price = 0
        for field in self._meta.fields:
            if str(field).split(".")[-1] != "ram":
                if isinstance(field, models.ForeignKey) and not isinstance(field, models.OneToOneField):
                    related_obj = getattr(self, field.name)
                    print(related_obj)
                    if related_obj and hasattr(related_obj, "product") and hasattr(related_obj.product, "unit_price"):
                        final_price += related_obj.product.unit_price
        

        final_price += (self.ram.product.unit_price * self.ram_quantity)

        if self.product:
            self.product.unit_price = final_price

            self.product.save()

        assign_category(instance=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name}"
    class Meta:
        verbose_name="PC"
        verbose_name_plural="PCs"
