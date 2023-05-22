from django.db.models import Sum
from django.http import HttpResponse
from grocery_assistant.models import IngredientRecipe


def download_product(self, request, author):
    """ Сохранение списка рецептов в формате txt """
    sum_group_by_ingredient = IngredientRecipe.objects.filter(
        recipes__shoping_list__user=author
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(
        amount=Sum('amount', distinct=True)).order_by('amount')
    file_txt = """  Продуктовый помошник / Grocery_Assistant
    Автор - Уланов Павел\n
    Продукты для покупок:\n"""
    val_count = 0
    for ingr in sum_group_by_ingredient:
        val_count += 1
        file_txt += (
            f'{val_count}. {ingr["ingredient__name"]} - '
            f'{ingr["amount"]} '
            f'{ingr["ingredient__measurement_unit"]}\n'
        )
    filename = 'shopping_list.txt'
    response = HttpResponse(file_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
