from django.db.models import Sum
from django.http import HttpResponse

from grocery_assistant.models import Ingredients_list


def download_product(self, request, author):
    # Скачивание списка продуктов для выбранных рецептов пользователя.
    sum_group_by_ingr_id = Ingredients_list.objects.filter(
        recipes_id__shoping_list__user_id=author
    ).values(
        'ingr_id__ingr_name', 'ingr_id__measurement_unit'
    ).annotate(
        quantity=Sum('quantity', distinct=True)).order_by('quantity')
    file_txt = """  Продуктовый помошник / Grocery_Assistant
    Автор - Уланов Павел\n
    Продукты для покупок:\n"""
    val_count = 0
    for ingr in sum_group_by_ingr_id:
        val_count += 1
        file_txt += (
            f'{val_count}. {ingr["ingr_id__ingr_name"]} - '
            f'{ingr["quantity"]} '
            f'{ingr["ingr_id__measurement_unit"]}\n'
        )
    filename = 'shopping_list.txt'
    response = HttpResponse(file_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
