from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.contenttypes.models import ContentType

from .models import Comment


# Create your views here.

# Ajax creating comment.
def delete_comment(request):
    if request.method == 'POST':
        try:
            comment_id = int(request.POST.get("comment_id"))
        except:
            comment_id = None

        response_data = {
            'is_success': False,
            'parent': False,
            'parent_comment_id': None,
            'parent_comment_children': None,
        }

        parent_comment = None

        if comment_id is not None:
            comment_qs = Comment.objects.filter(id=comment_id)
            if comment_qs.exists() and comment_qs.count() == 1:
                comment_to_delete = comment_qs.first()
                if comment_to_delete.children.count() != 0:
                    response_data["parent"] = True
                    for child in comment_to_delete.children:
                        child.delete()
                else:
                    parent_comment = comment_to_delete.parent

                comment_to_delete.delete()
                response_data['is_success'] = True
                response_data['parent_id'] = str(comment_id)
                if parent_comment is not None:
                    response_data['parent_comment_id'] = parent_comment.id
                    response_data['parent_comment_children'] = parent_comment.children.count()
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


def create_comment(request):
    if request.method == 'POST':
        try:
            object_id = int(request.POST.get("object_id"))
            type = request.POST.get("content_type")
            comment_content = request.POST.get("comment_content")
            parent_id = request.POST.get("parent_id")
        except:
            return HttpResponseBadRequest()

        c_type = ContentType.objects.get(model=type)
        parent_obj = None
        if parent_id is not None:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment = Comment.objects.create(
                user=request.user,
                content_type=c_type,
                object_id=object_id,
                content=comment_content,
                parent=parent_obj
            )

        if new_comment.user.get_full_name:
            name = new_comment.user.get_full_name()
        else:
            name = new_comment.user

        child_amount = 0
        if parent_obj is not None:
            child_amount = parent_obj.children.count()

        response_data = {
            "success": True,
            "name": name,
            "photo_url": new_comment.user.profile.profile_image_url(),
            "comment_id": new_comment.id,
            "children": child_amount,
        }

        return JsonResponse(response_data)

