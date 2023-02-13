import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from matplotlib import category

from ads.models import Category, Ad
from users.models import User

PAGE_NUMBER = 4


# def cool(request):
#     return JsonResponse({"status": "ok"})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({'id':category.pk,
                             "name": category.name}, safe=False)


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by("name").all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id":cat.id, "name": cat.name} for cat in self.object_list], safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        new_cat = Category.objects.create(name=data["name"],)
        return JsonResponse({"id":new_cat.pk, "name": new_cat.name}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()
        return JsonResponse({"id":self.object.pk, "name": self.object.name}, safe=False)

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        cat = self.get_object()
        cat_id = cat.id
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": cat_id}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdListCreateView(View):
    def get(self, request):
        response = []
        for ad in Ad.objects.all():
            response.append(
                {"id": ad.pk,
                 "name": ad.name,
                 "author": ad.author,
                 "price": ad.price}
            )
        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        ad = Ad.objects.create(
            name=data["name"],
            author=data["author"],
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            address=data["address"]
        )

        return JsonResponse({"id":ad.pk,
                             "name":ad.name,
                             "author":ad.author,
                             "price": ad.price,
                             "description":ad.description,
                             "is_published":ad.is_published}, safe=False)

class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({"id":ad.pk,
                             "name": ad.name,
                             "author": ad.author.username,
                             "price": ad.price,
                             "description": ad.description,
                             "category": ad.category.name,
                             "is_published": ad.is_published
                             }, safe=False)


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by("-price").select_related("author")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, PAGE_NUMBER)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return JsonResponse(
            {"total": page_obj.paginator.count,
             "num_pages": page_obj.paginator.num_pages,
             "items": [{"id": ad.pk,
                        "name":ad.name,
                        "author_id": ad.author_id,
                        "author": ad.author.first_name,
                        "price": ad.price,
                        "description": ad.description,
                        "is_published": ad.is_published,
                        "category_id": ad.category_id,
                        "image": ad.image.url if ad.image else None}for ad in page_obj]}
        )

@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, username=data["username"])
        category = get_object_or_404(Category, name=data["category"])

        ad = Ad.objects.create(
            name=data["name"],
            author=author,
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            category=category,
        )

        return JsonResponse({"id": ad.pk,
                             "name": ad.name,
                             "author": ad.author.username,
                             "category": ad.category.name,
                             "price": ad.price,
                             "description": ad.description,
                             "is_published": ad.is_published
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def patch(self, request,*args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.author = get_object_or_404(User, username=data["username"])
        self.object.category = get_object_or_404(Category, name=data["category"])
        self.object.name=data["name"],
        self.object.price=data["price"],
        self.object.is_published=data["is_published"],
        self.object.description=data["description"],

        return JsonResponse({"id": self.object.pk,
                             "name": self.object.name,
                             "author": self.object.author.username,
                             "category": self.object.category.name,
                             "price": self.object.price,
                             "description": self.object.description,
                             "is_published": self.object.is_published
                             }, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        ad = self.get_object()
        ad_id = ad.id
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": ad_id}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpload(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse({"name": self.object.name, "image": self.object.image.url})

