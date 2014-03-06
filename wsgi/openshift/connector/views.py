from django.shortcuts import render

# Create your views here.
class ProfileView(DetailView):
    model = Member
    template_name = 'members/profile.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        # NOTE: "year" is a field lookup type so must use "year__exact" instead
        project_members = ProjectMember.objects.filter(member__pk=self.kwargs.get('pk', None)).order_by('-project__year')
        context['project_groups'] = [ {'year': x, 'project_members': project_members.filter(project__year__exact=x).order_by('project__title') } for x in project_members.values_list('project__year', flat=True).distinct() ]

        context['recent_blogs'] = BlogPost.objects.filter(author__pk=self.kwargs.get('pk', None)).order_by('-date')[:3]

        return context