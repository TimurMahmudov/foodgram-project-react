from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response


class CreateDestroyObjView(generics.CreateAPIView,
                           generics.DestroyAPIView,
                           viewsets.ViewSet):
    serializer_class = None
    response_serializer = None
    model_obj = None
    model_connection = None

    def _get_obj(self, obj_id):
        return get_object_or_404(self.model_obj, pk=obj_id)

    def _get_data(self, request, id):
        return {
            f'{self.model_connection._meta.fields[1].name}': id,
            'user': request.user.id
        }

    def create(self, request, id):
        obj = self._get_obj(id)
        obj_serializer = self.response_serializer(obj,
                                                  context={'request': request})
        serializer = self.get_serializer(
            data=self._get_data(request, obj.id),
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(obj_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        obj = self._get_obj(id)
        user = request.user
        dict_data = {
            self.model_connection._meta.fields[1].name: obj,
            self.model_connection._meta.fields[2].name: user
        }
        connect = get_object_or_404(
            self.model_connection,
            **dict_data
        )
        connect.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
