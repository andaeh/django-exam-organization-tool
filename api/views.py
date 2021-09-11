from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from exam_organization.models import Task, Topic, Grade, Faculty

from .pagination import StandardResultsSetPagination
from .serializers import TaskSerializer, GradeSerializer, TopicSerializer, FacultySerializer


# Create your views here.
class TaskListing(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()

        keywords = self.request.query_params.get('keywords', None)
        topic = self.request.query_params.get('topic', None)
        grade = self.request.query_params.get('grade', None)
        faculty = self.request.query_params.get('faculty', None)

        # Filter nach Topic
        if topic:
            queryset = queryset.filter(topic__id__contains=topic).distinct()
        
        # Filter nach Grade
        if grade:
            queryset = queryset = queryset.filter(topic__grade__id__contains=grade).distinct()

        # Filter nach Faculty
        if faculty:
            queryset = queryset.filter(topic__faculty__id__contains=faculty).distinct()

        if keywords:
            keywords = keywords.split(' ')
            querylist = Task.objects.none()
            for keyword in keywords:
                querylist |= queryset.filter(
                    Q(headline__contains=keyword)
                    | Q(description__contains=keyword)
                    | Q(tags__name__contains=keyword)
                ).distinct()
            queryset = querylist

        return queryset


class EigeneTaskListing(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)
        
        keywords = self.request.query_params.get('keywords', None)
        topic = self.request.query_params.get('topic', None)
        grade = self.request.query_params.get('grade', None)
        faculty = self.request.query_params.get('faculty', None)

        # Filter nach Topic
        if topic:
            queryset = queryset.filter(topic__id__contains=topic).distinct()
        
        # Filter nach Grade
        if grade:
            queryset = queryset = queryset.filter(topic__grade__id__contains=grade).distinct()

        # Filter nach Faculty
        if faculty:
            queryset = queryset.filter(topic__faculty__id__contains=faculty).distinct()

        if keywords:
            keywords = keywords.split(' ')
            querylist = Task.objects.none()
            for keyword in keywords:
                querylist |= queryset.filter(
                    Q(headline__contains=keyword)
                    | Q(description__contains=keyword)
                    | Q(tags__name__contains=keyword)
                ).distinct()
            queryset = querylist

        return queryset



class FacultyListing(ListAPIView):
    serializer_class = FacultySerializer

    def get_queryset(self):
        topic_ids = Task.objects.all().values_list('topic').distinct()
        topic_ids = [i[0] for i in topic_ids]
        topics = Topic.objects.none()
        for id in topic_ids:
            topics |= Topic.objects.filter(id=id)

        faculty_ids = topics.all().values_list('faculty').distinct()
        faculty_ids = [i[0] for i in faculty_ids]
        faculties = Faculty.objects.none()
        for id in faculty_ids:
            faculties |= Faculty.objects.filter(id=id)

    
        return faculties
        

        return topics



class GradeListing(ListAPIView):
    serializer_class = GradeSerializer

    def get_queryset(self):
        faculty = self.request.query_params.get('faculty', None)

        topic_ids = Task.objects.all().values_list('topic').distinct()
        topic_ids = [i[0] for i in topic_ids]
        topics = Topic.objects.none()
        for id in topic_ids:
            topics |= Topic.objects.filter(id=id)
        if faculty and not faculty == "all":
            topics = topics.filter(faculty=faculty)

        grade_ids = topics.all().values_list('grade').distinct()
        grade_ids = [i[0] for i in grade_ids]
        grades = Grade.objects.none()
        for id in grade_ids:
            grades |= Grade.objects.filter(id=id)

    
        return grades




class TopicListing(ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        grade = self.request.query_params.get('grade', None)
        faculty = self.request.query_params.get('faculty', None)

        topic_ids = Task.objects.all().values_list('topic').distinct()
        topic_ids = [i[0] for i in topic_ids]
        topics = Topic.objects.none()
        for id in topic_ids:
            topics |= Topic.objects.filter(id=id)
        
        if grade and not grade == "all":
            topics = topics.filter(grade=grade)

        if faculty and not faculty == "all":
            topics = topics.filter(faculty=faculty)


        return topics


@api_view(http_method_names=['GET'])
def own_task_listing(request):
    pagination_class = StandardResultsSetPagination()
    queryset = Task.objects.filter(created_by=request.user)
    list = []

    keywords = request.query_params.get('keywords', None)

    if keywords:
        keywords = keywords.split(' ')
        own_tasks = Task.objects.filter(created_by=request.user)
        queryset = Task.objects.none()
        for keyword in keywords:
            queryset |= own_tasks.filter(
                Q(headline__contains=keyword)
                | Q(description__contains=keyword)
                | Q(tags__name__contains=keyword)
            ).distinct()

    for row in queryset:
        list.append({
            'id': row.id,
            'headline': row.headline,
            'description': row.description,
            'created_by': row.created_by.last_name,
            'edited_by': row.edited_by.last_name
        })

    return Response(list)

