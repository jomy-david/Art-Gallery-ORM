from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from random import randint
from .models import artist_list,category_list,comments,commentspam,like_list,logintb,post_list,user_list,test

# Create your views here.

# Home
lis=['user','admin','artist']

def home(request):
    context = {}
    # Category Select For navbar
    context['cat']=category_list.objects.all()
    # Top 3 Liked
    top_likes = post_list.objects.filter(status='1').order_by('-likes')
    # home Page Posts

    context['posts']=post_list.objects.filter(status='1')
    if len(top_likes)>3:
        context['top_like']=top_likes[0:3]
    else:
        context['top_like']=top_likes
    # Initializing Posts in a Category
    for i in context['cat']:
        p=0
        for j in context['posts']:
            if i.cat_id==j.cat_id:
                p+=1
        p = str(p)        
        post_update = category_list.objects.get(cat_id=i.cat_id)
        post_update.posts=p
        post_update.save(update_fields=['posts'])

    try:   
        if 'admin' in request.session:
            context['user_data']=logintb.objects.get(user_id=request.session['admin'])
            print(context['user_data'])
            return render(request,'main/index.html',context)
        elif 'artist' in request.session:
            context['user_data']=logintb.objects.get(user_id=request.session['artist'])
            print(context['user_data'])
            return render(request,'main/index.html',context)
        elif 'user' in request.session:
            context['user_data']=logintb.objects.get(user_id=request.session['user'])
            print(context['user_data'])
            return render(request,'main/index.html',context)
        else:
            return render(request,'main/index.html',context)
    except:
        print('d')
        return render(request,'main/index.html',context)

def Gallery(request):
    context = {}
    if request.GET:
        id = request.GET['id']
        context['cat']=category_list.objects.all()
        context['post']= post_list.objects.filter(cat_id=id)
        context['cat_id']=category_list.objects.values('name').get(cat_id=id)
        for i in lis:
            try:
                context['user_data']=logintb.objects.get(user_id=request.session[i])
                break
            except:
                continue
        return render(request,'main/gallery.html',context)
    return HttpResponseRedirect('error')

def post(request):
    context={}
    
    if request.session.keys():
        if request.GET.get('id'):
            id = request.GET['id']
            context['cat']=category_list.objects.all()

            context['post']=post_list.objects.get(post_id=id)
            # Updating Likes Count

            post_like = like_list.objects.values('user_id').filter(post_id=id)
            likes_count=str(len(post_like))

            post_list.objects.filter(post_id=id).update(likes=likes_count)
            # Updating Comments Count

            comment = comments.objects.filter(post_id=id)
            context['comments']=comment
            comment_count=str(len(comment))
            context['comment_count']=comment_count

            post_list.objects.filter(post_id=id).update(comments=comment_count)

            context['likes']=likes_count

            post_details = post_list.objects.get(post_id=id)

            artist_data=artist_list.objects.get(artist_id=post_details.artist_id)
            context['artist_data']=artist_data
            try:
                context['user_data']=logintb.objects.get(user_id=request.session['admin'])
                if request.session['admin'] in post_like:
                    context['like'] = True
                else:
                    context['like'] = False
                return render(request,'main/post.html',context)
            except:
                try:
                    
                    context['user_data']=logintb.objects.get(user_id=request.session['artist'])

                    if request.session['artist'] in post_like:
                        context['like'] = True
                    else:
                        context['like'] = False
                    return render(request,'main/post.html',context)
                except:
                    try:
                        
                        context['user_data']=logintb.objects.get(user_id=request.session['user'])

                        if request.session['user'] in post_like:
                            context['like'] = True
                        else:
                            context['like'] = False
                        return render(request,'main/post.html',context)
                    except:
                        return render(request,'main/post.html',context)
    
    return HttpResponseRedirect('Login')

def likePost(request):
    context={}
    if request.GET.get('id'):
        post_id = str(request.GET['id'])
        if 'artist' in request.session.keys():
            user_id = request.session['artist']
        elif 'admin' in request.session.keys():
            user_id = request.session['admin']
        elif 'user' in request.session.keys():
            user_id = request.session['user']
        else:
            return HttpResponseRedirect('Login')

        like = like_list.objects.filter(post_id=post_id,user_id=user_id)
        if like:
            like_list.objects.get(post_id=post_id,user_id=user_id).delete()
        else:

            new_like = like_list(user_id=user_id,post_id=post_id)
            new_like.save()
        return HttpResponseRedirect('viewPost?id='+post_id)
    
def addComment(request):
    context={}
    if request.GET.get('post'):
        post_id = str(request.GET.get('post'))
        comment = request.GET.get('comment')
        if 'artist' in request.session.keys():
            user_id = request.session['artist']
        elif 'admin' in request.session.keys():
            user_id = request.session['admin']
        elif 'user' in request.session.keys():
            user_id = request.session['user']
        else:
            return HttpResponseRedirect('Login')
        # Comment Check for spam

        spam_check = comments.objects.filter(user_id=user_id,post_id=post_id,comment=comment)

        if spam_check:
            return HttpResponseRedirect('viewPost?id='+post_id)
        else:

            new_comment = comments(post_id=post_id,user_id=user_id,comment=comment,spam='0')
            new_comment.save()
            return HttpResponseRedirect('viewPost?id='+post_id)

def spamComment(request):
    context={}
    if request.GET.get('comment_id'):
        comment_id = request.GET.get('comment_id')
        post_id=request.GET.get('post_id')
        if 'artist' in request.session.keys():
            user_id = request.session['artist']
        elif 'admin' in request.session.keys():
            user_id = request.session['admin']
        elif 'user' in request.session.keys():
            user_id = request.session['user']
        else:
            return HttpResponseRedirect('Login')

        spam_check = commentspam.objects.filter(comment_id=comment_id,user_id=user_id)
        if spam_check:
            return HttpResponseRedirect('viewPost?id='+post_id)
        else:

            new_spam = commentspam(comment_id=comment_id,user_id=user_id)
            new_spam.save()
            spam = comments.objects.values('spam').get(id=comment_id)+1
            comments.objects.filter(id=comment_id).update(spam=spam)
            return HttpResponseRedirect('viewPost?id='+post_id)
        
def ArtistsList(request):
    context={}

    post_data = post_list.objects.filter(status=1)

    artists_data= artist_list.objects.values_list('artist_id')
    print(artists_data)
    for artist in artists_data:
        counter = 0
        for post in post_data:
            if artist[0]==post.artist_id:
                counter+=1

        artist_list.objects.filter(artist_id=artist[0]).update(posts=str(counter))
 
    context['artist_data']=artist_list.objects.all()
    for i in lis:
        try:
            context['user_data']=logintb.objects.get(user_id=request.session[i])
            break
        except:
            continue
    return render(request,'main/artists.html',context)
    
    
    
# Registration and login

def register(request):
    if request.POST:
        if request.POST.get("submit")=="artist":
            if request.POST.get("password")==request.POST.get("c_password"):
                name = request.POST.get("name")
                id = request.POST.get("artist_id")

                check_id = artist_list.objects.values('artist_id').filter(artist_id=id)
                if check_id:
                    return render(request,'main/register.html',{'error':"Id Already Exits"})
                d_name = request.POST.get("d_name")
                email = request.POST.get("email")
                contact = request.POST.get("contact")
                address = request.POST.get("address")
                gender = request.POST.get("gender")
                password = request.POST.get("password")
                fs = FileSystemStorage()
                image = request.FILES['pic']
                image_name = id+str(randint(1,10000))+image.name
                fs.save("artist/profile_pic/"+image_name,image)

                new_artist = artist_list(name=name,artist_id=id,email=email,password=password,profile_pic=image_name,contact=contact,gender=gender,display_name=d_name,address=address,status='0',posts=0)
                new_artist.save()
                

                new_login = logintb(user_id=id,user_type='artist',status='0',password=password)
                new_login.save()
                return render(request,'main/login.html',{'msg':"Registration Successful"})
            
        elif request.POST.get("submit")=="user":
            if request.POST.get("password")==request.POST.get("c_password"):
                name = request.POST.get("name")
                id = request.POST.get("user_id")

                check_id = user_list.objects.values('user_id').filter(user_id=id)
                if check_id:
                    return render(request,'main/register.html',{'error':"Id Already Exits"})
                email = request.POST.get("email")
                contact = request.POST.get("contact")
                gender = request.POST.get("gender")
                password = request.POST.get("password")
                image_name="blank-profile-picture-973460_1280.png"
                
                new_user = user_list(name=name,user_id=id,email=email,password=password,contact=contact,profile_pic=image_name,gender=gender,status='1')
                new_user.save()

                new_login = logintb(user_id=id,user_type='user',status='1',password=password)
                new_login.save()
                return render(request,'main/login.html',{'msg':"Registration Successful"})
    return render(request,'main/register.html')

def login(request):
    if 'admin' in request.session.keys():
        return HttpResponseRedirect('home')
    elif 'artist' in request.session.keys():
        return HttpResponseRedirect('home')
    elif 'user' in request.session.keys():
        return HttpResponseRedirect('home')
    else:
        context={}
        if request.POST:
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = logintb.objects.get(user_id=user_name,password=password)
                print(user.user_type)
                if user.user_type:
                    if user.user_type=='artist' and user.status==1:
                        print(user.user_id)
                        request.session['artist']=user.user_id                
                        return HttpResponseRedirect('home')
                    elif user.user_type=='admin':
                        request.session['admin']=user.user_id
                        return HttpResponseRedirect('administrator')
                    elif user.user_type=='user':
                        request.session['user']=user.user_id
                        return HttpResponseRedirect('home')
                    else:
                        return render(request,'main/login.html',{'error':"Invalid Credentials"})
            except:
                    return render(request,'main/login.html',{'error':"Invalid Credentials"})

        return render(request,'main/login.html')

def logout(request):
    if 'artist' in request.session.keys():
        del request.session['artist']
    elif 'admin' in request.session.keys():
        del request.session['admin']
    elif 'user' in request.session.keys():
        del request.session['user']
    return HttpResponseRedirect('home')


# Admin

def admin(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        artist_aprovals = artist_list.objects.filter(status=0)
        post_aprovals = post_list.objects.filter(status=0)
        context['post_len']=len(post_aprovals)
        context['posts']=post_aprovals
        context['aprovals']=artist_aprovals
        context['aprovals_len']=len(artist_aprovals)
        return render(request,'administrator/index.html',context)
    
def adminEdit(request):
    context={}
    uid = request.session['admin']
    context['admin']=request.session['admin']
    if request.POST:
        if request.POST.get("password")==request.POST.get("c_password"):
            id = request.POST.get("id")
            if id!=uid:
                check_id = logintb.objects.values('user_id').filter(user_id=id)
                if check_id:
                    context['error']="User ID Already Exists"
                    return render(request,'administrator/editDetails.html',context)
            password = request.POST.get("password")
            logintb.objects.filter(user_id=uid).update(user_id=id,password=password)
            user_id=logintb.objects.values('user_id').get(user_id=id)
            request.session['admin']=user_id['user_id']
            return HttpResponseRedirect('adminEdit')
    context['details']=logintb.objects.get(user_id=uid)
    return render(request,'administrator/editDetails.html',context)

def artistAp(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        artist_aprovals = artist_list.objects.filter(status=0)
        context['aprovals']=artist_aprovals
        return render(request,'administrator/artistAprovals.html',context)
    return render(request,'error')

def viewArtist(request):
    context ={}
    if request.session['admin']:
        id = request.GET.get('id')
        context['admin']=request.session['admin']
        artist_details = artist_list.objects.get(artist_id=id)
        context['details']=artist_details
        return render(request,'administrator/artistView.html',context)
    return render(request,'error')

def aproveArtist(request):
    if request.session['admin']:
        id = request.GET.get('id')
        logintb.objects.filter(user_id=id).update(status='1')
        artist_list.objects.filter(artist_id=id).update(status='1')
        return HttpResponseRedirect('artistAprovals')
    return HttpResponseRedirect('error')

def denyArtist(request):
    if request.session['admin']:
        id = request.GET.get('id')
        logintb.objects.filter(user_id=id).update(status='2')
        artist_list.objects.filter(artist_id=id).update(status='1')
        return HttpResponseRedirect('artistAprovals')
    return HttpResponseRedirect('error')

def artistList(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        context['artist_list']=artist_list.objects.all()
        return render(request,'administrator/artistList.html',context)
    return render(request,'error')

def editGallery(request):
    if request.POST:
        cat_name=request.POST.get('cat')
        cat_obj = category_list(name=cat_name,posts='0')
        cat_obj.save()
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        context['category']= category_list.objects.all()
        return render(request,'administrator/categoryEdit.html',context)
    return render(request,'error')

def delCat(request):
    context={}
    if request.session['admin']:
        if request.GET.get('id'):
            did = request.GET.get('id')
            post_check = category_list.objects.get(cat_id=did)
            
            if post_check.posts>0:               
                context['admin']=request.session['admin']
                context['category']=category_list.objects.all()
                context['msg']="Cannot Delete Categories containing posts"
                return render(request,'administrator/categoryEdit.html',context)
            else:

                category_list.objects.get(cat_id=did).delete()
                return HttpResponseRedirect('editGallery')

def postAp(request):
    context ={}
    if request.session['admin']:
        context['admin']=request.session['admin']
        context['aprovals']=post_list.objects.filter(status=0)
        return render(request,'administrator/postAprovals.html',context)
    return render(request,'error')

def aprovePost(request):
    if request.session['admin']:
        id = request.GET.get('id')
        post_list.objects.filter(post_id=id).update(status='1')
        return HttpResponseRedirect('postAprovals')
    return HttpResponseRedirect('error')

def denyPost(request):
    if request.session['admin']:
        id = request.GET.get('id')
        post_list.objects.filter(post_id=id).update(status='2')
        return HttpResponseRedirect('postAprovals')
    return HttpResponseRedirect('error')

# Artist

def artistHome(request):
    context ={}
    if request.session['artist']:
        id = request.session['artist']
        context['artist']=artist_list.objects.get(artist_id=id)
        context['data'] = post_list.objects.filter(artist_id=id)
        return render(request,'artist/myGallery.html',context)

def artistProfile(request):
    context={}
    if request.GET.get('id'):
        id = request.GET.get('id')
        context['cat']=category_list.objects.all()
        context['gallery']=post_list.objects.filter(artist_id=id,status=1)
        context['len_gallery']=len(context['gallery'])
        context['artist_data']=artist_list.objects.get(artist_id=id)
        for i in lis:
            try:
                context['user_data']=logintb.objects.get(user_id=request.session[i])
                break
            except:
                continue
        return render(request,'artist/myProfile.html',context)
    else:
        return HttpResponseRedirect('error')
    
    
def editArtist(request):
    context ={}
    uid = request.session['artist']
    if request.session['artist']:
        if request.POST:
            name = request.POST.get("name")
            id = request.POST.get("user_id")
            if id != uid:
                try:
                    check_id = logintb.objects.values('user_id').get(user_id=id)
                    context['msg']="userid already exists"
                    context['details']=user_list.objects.get(user_id=uid)
                    return render(request,'user/editProfile.html',context)
                except:
                    pass
            email = request.POST.get("email")            
            contact = request.POST.get("contact")
            password = request.POST.get("password")
            if request.POST.get('img'):
                fs = FileSystemStorage()
                image = request.FILES['img']
                image_name = id+str(randint(1,10000))+image.name
                artist_list.objects.filter(artist_id=uid).update(name=name,artist_id=id,email=email,contact=contact,password=password,profile_pid=image_name)
            else:
                artist_list.objects.filter(artist_id=uid).update(name=name,artist_id=id,email=email,contact=contact,password=password)          

            logintb.objects.filter(user_id=uid).update(user_id=id,password=password)
            if id!=uid:
                post_list.objects.filter(artist_id=uid).update(artist_id=id)
                comments.objects.filter(user_id=uid).update(user_id=id)
                like_list.objects.filter(user_id=uid).update(user_id=id)
                commentspam.objects.filter(user_id=uid).update(user_id=id)
            print(id)
            
            request.session['artist']=id
            context['msg']="updated"

        context['artist']=artist_list.objects.get(artist_id=request.session['artist'])

        context['details']=artist_list.objects.get(artist_id=request.session['artist'])
        return render(request,'artist/editProfile.html',context)
    return render(request,'error')

def addPost(request):
    context={}
    if request.session['artist']:
        id = request.session['artist']
        context['artist']=artist_list.objects.get(artist_id=id)
        artistid = request.session['artist']
        artist_data = artist_list.objects.get(artist_id=artistid)
        context['cat']=category_list.objects.all()
        if request.POST:
            title = request.POST.get('title')
            cat = request.POST.get('cat')
            print(cat)
            print(title)
            cat_id = category_list.objects.values('cat_id').get(name=cat)
            
            fs = FileSystemStorage()
            image = request.FILES['img']
            image_name = artist_data.artist_id+str(randint(1,10000))+image.name
    
            new_post = post_list(file_name=image_name,artist_name=artist_data.name,artist_id=artist_data.artist_id,category=cat,cat_id=cat_id['cat_id'],status='0',title=title,likes='0',comments='0')
            new_post.save()
            fs.save("artist/uploads/"+image_name,image)
            return HttpResponseRedirect('artistHome')
        return render(request,'artist/addPost.html',context)
    

# User

def userHome(request):
    context={}
    try:
        if request.session['user']:
            context['user']=user_list.objects.get(user_id=request.session['user'])
            try:
                like_posts=like_list.objects.values_list('post_id').get(user_id=request.session['user'])
                liked_list=[]
                for id in like_posts:
                    get = post_list.objects.get(post_id=id)
                    liked_list.append(get)
                
                context['data']=liked_list
                return render(request,'user/index.html',context)
            except:
                return render(request,'user/index.html',context)
    except:
        return render(request,'main/login.html')

def editUser(request):
    context ={}
    uid = request.session['user']
    if request.session['user']:
        if request.POST:
            name = request.POST.get("name")
            id = request.POST.get("user_id")
            if id != uid:
                try:
                    check_id = logintb.objects.values('user_id').get(user_id=id)
                    context['msg']="userid already exists"
                    context['details']=user_list.objects.get(user_id=request.session['user'])
                    return render(request,'user/editProfile.html',context)
                except:
                    pass
            email = request.POST.get("email")            
            contact = request.POST.get("contact")
            password = request.POST.get("password")
            try:
                if request.FILES['img']:
                    fs = FileSystemStorage()
                    image = request.FILES['img']
                    image_name = id+str(randint(1,10000))+image.name
                    fs.save("user/profile_pic/"+image_name,image)
                    user_list.objects.filter(user_id=uid).update(name=name,user_id=id,email=email,contact=contact,password=password,profile_pic=image_name)
            except:
                user_list.objects.filter(user_id=uid).update(name=name,user_id=id,email=email,contact=contact,password=password)
            

            logintb.objects.filter(user_id=uid).update(user_id=id,password=password)
            if id!=uid:
                comments.objects.filter(user_id=uid).update(user_id=id)
                like_list.objects.filter(user_id=uid).update(user_id=id)
                commentspam.objects.filter(user_id=uid).update(user_id=id)
            request.session['user']=id
            context['msg']="updated"
        context['user']=user_list.objects.get(user_id=request.session['user'])

        context['details']=user_list.objects.get(user_id=request.session['user'])

        return render(request,'user/editProfile.html',context)
    return render(request,'error')

# Error Page
def error(request):
    return render(request,'404_error.html')

def test(request):
    if request.session['user']:
        print("ok")



