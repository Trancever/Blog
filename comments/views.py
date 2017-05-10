from django.http import JsonResponse

from .models import Comment


# Create your views here.

# Ajax creating comment.
def delete_comment(request):
    if request.method == 'POST':
        try:
            comment_id = int(request.POST.get("comment_id"))
        except:
            comment_id = None
        response_data = {}
        print(comment_id)

        response_data['is_success'] = False
        response_data['parent'] = False

        if comment_id is not None:
            comment_qs = Comment.objects.filter(id=comment_id)
            if comment_qs.exists() and comment_qs.count() == 1:
                comment_to_delete = comment_qs.first()
                if comment_to_delete.children.count() != 0:
                    response_data["parent"] = True
                    for child in comment_to_delete.children:
                        child.delete()
                comment_to_delete.delete()
                response_data['is_success'] = True
                response_data['parent_id'] = str(comment_id)
                return JsonResponse(response_data)

    return JsonResponse(response_data)



# Ajax editing comment.
def edit_comment(request):
    if request.method == 'POST':
        try:
            comment_id = int(request.POST.get("comment_id"))
            comment_content = str(request.POST.get("comment_content"))
        except:
            comment_id = None
            comment_content = None

        response_data = {}

        response_data['is_success'] = False
        response_data['comment_content'] = ""

        if comment_id is not None:
            comment_qs = Comment.objects.filter(id=comment_id)
            if comment_qs.exists() and comment_qs.count() == 1:
                comment_to_edit = comment_qs.first()
                comment_to_edit.content = comment_content
                comment_to_edit.save(update_fields=["content", "updated"])
                response_data['is_success'] = True
                response_data['comment_content'] = comment_content
                response_data['comment_id'] = comment_id
                return JsonResponse(response_data)

    return JsonResponse(response_data)