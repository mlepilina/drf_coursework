from django.core.paginator import Paginator


def paginate(query, per_page, page_number):
    paginator = Paginator(query, per_page=per_page)
    page = paginator.get_page(page_number)
    return {
        'list': page.object_list,
        'current_page': page.number,
        'next_page': page.next_page_number() if page.has_next() else page.number,
        'previous_page': page.previous_page_number() if page.has_previous() else page.number,
    }
