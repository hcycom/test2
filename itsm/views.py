from django.shortcuts import render,HttpResponse
import core
import json
import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import asset_handle,utils
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@csrf_exempt
@utils.token_required
def asset_report(request):

    print(request.GET)
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid():
            ass_handler.data_inject()
            #return HttpResponse(json.dumps(ass_handler.response))

        return HttpResponse(json.dumps(ass_handler.response))
        #return render(request,'assets/asset_report_test.html',{'response':ass_handler.response})
        #else:
            #return HttpResponse(json.dumps(ass_handler.response))

    return HttpResponse('--3333test--')

def test(r):
    pass
@csrf_exempt
def asset_with_no_asset_id(request):
    print request.method,"*********************"
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        res = ass_handler.get_asset_id_by_sn()
        print res
        #return render(request,'assets/acquire_asset_id_test.html',{'response':res})
        return HttpResponse(json.dumps(res))



def new_assets_approval(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        approved_asset_list = request.POST.getlist('approved_asset_list')
        print approved_asset_list
        approved_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)

        response_dic = {}
        for obj in approved_asset_list:
            print obj.data
            request.POST['asset_data'] = obj.data
            ass_handler = core.Asset(request)
            if ass_handler.data_is_valid_without_id():
                ass_handler.data_inject()
                obj.approved = True
                obj.save()

            response_dic[obj.id]= ass_handler.response
        return render(request,'assets/new_assets_approval.html',{'new_assets':approved_asset_list,'response_dic':response_dic})
    else:
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_assets = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request,'assets/new_assets_approval.html',{'new_assets':new_assets})


def asset_report_test(request):

    return render(request,'assets/asset_report_test.html')

def acquire_asset_id_test(request):

    return render(request,'assets/acquire_asset_id_test.html')

def asset_list(request):

    return render(request,'assets/assets.html')

@login_required
def get_asset_list(request):

    asset_dic = asset_handle.fetch_asset_list()
    print(asset_dic)

    return HttpResponse(json.dumps(asset_dic,default=utils.json_date_handler))



@login_required
def asset_event_logs(request,asset_id):
    if request.method == "GET":
        log_list = asset_handle.fetch_asset_event_logs(asset_id)
        return HttpResponse(json.dumps(log_list,default=utils.json_datetime_handler))

@login_required
def asset_detail(request,asset_id):

    if request.method == "GET":
        try:
            asset_obj = models.Asset.objects.get(id=asset_id)

        except ObjectDoesNotExist,e:
            return render(request,'assets/asset_detail.html',{'error':e})
        return render(request,'assets/asset_detail.html',{"asset_obj":asset_obj})


def asset_base_all(request):

    return render(request,'assets/assets.html')