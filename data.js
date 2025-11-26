function poster(url,data,cb) {
    var s=''
    var camma=''
    for (var key of Object.keys(data)) {
        var val=data[key];
        val=encodeURIComponent(val);
        s+= camma + key +'='+val;
        camma='&'
    }
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'},
        body: s
    })
    .then(response => response.text() )
    .then(data     => cb(data) )
    .catch(error   => console.log(error))
}
function toTicks(a) {
    var dic={}
    var cats=[]
    var comma=''
    for (var item of a) {
        // console.log(item.testCat);
        if (!(item.testCat in dic)) {
            dic[item.testCat]=''
            cats.push({catname:item.testCat})
            comma=''
        }
        var atom=comma+item.name
        dic[item.testCat]+= atom;
        comma=', '
    }
    return sortTicks(dic);
}
function sortTicks(dic){
    var phoneinfo = getCache('phoneinfo');
    var cats=phoneinfo.details.testcats;
    var c=[]
    for (cat of cats) {
        var items=dic[cat.name];
        // items=items?items:''
        if (items) {
            c.push({catname:cat.name,items:items})
        }
    }
    // console.log(c);
    return c;
}
function toChecklist(a) {
    var dic={}
    var cats=[]
    for (var item of a) {
        // console.log(item.testCat);
        if (!(item.testCat in dic)) {
            dic[item.testCat]=[]
            cats.push({catname:item.testCat})
        }
        var atom={name:item.name,code:item.code}
        dic[item.testCat].push(atom)
    }
    // console.log(dic);
    for (var cat of cats) {
        // console.log(cat.testCat);
        cat.items=dic[cat.catname]
    }
    // console.log(cats);
    return cats;
}
function deCacheAll(){
    sessionStorage.clear()
}
function deCache(k) {
    sessionStorage.removeItem(k)
}
function setCache(k,o) {
    sessionStorage.setItem(k,bh(encodeURIComponent(JSON.stringify(o))))
}
function getCache(k) {
    var s=sessionStorage.getItem(k)
    return JSON.parse(decodeURIComponent(hb(s)))
}
function walk() {
    document.querySelectorAll('[name]').forEach((o,i)=>{
        // console.log(i,o);
    });
}
// var ff=filterTicks(testitems,anslist5)
// console.log(toTicks(ff));
function filterTicks(testitems,anlist) {
    var a= testitems.filter(o=>o.code in anlist)
    var b= a.map(o=>{
        return {testCat:o.testCat,name:o.name,code:o.code}
    })
    // console.log(b);
    return b;
}
function dollar(n){
    if (n==null || n==undefined) {
        return '$0'
    }
    return n>1000? '$'+String(Math.floor(n/1000))+','+String(n%1000).padStart(3,'0'):'$'+String(n)
}
function drawOrder(testitems,anslist){
    // depends on following html classes
    // phonestatusinfoinner
    // -phonestatusinfoinnerline
    // --phonestatusinfoinnertitle
    // --phonestatusinfoinnertext
    // .pricenumber2
    var tmp='<div id="tmp101" hidden>' + $('.phonestatusinfoinnerline')[0].outerHTML + '</div>';
    var items=filterTicks(testitems,anslist)
    var ticks=toTicks(items)
    $('body').append(tmp)
    var s=''
    for (var o of ticks) {
        $('#tmp101').find('.phonestatusinfoinnertitle').text(o.catname)
        $('#tmp101').find('.phonestatusinfoinnertext').text(o.items)
        var html = $('#tmp101').html()
        s+=html;
    }
    $('#tmp101').remove()
    $('.phonestatusinfoinner').html(s)
}

function drawPhoneInfo(phoneData) {
    if (phoneData.click==null) {
        phoneData.click=1
    }
    $('.detailphoneimg').attr("src", phoneData.photo)
    $('.detailphonebrand').text(phoneData.brand)
    $('.detailphonemodel').text(phoneData.model)
    $('.detailphonecapacity').text(phoneData.capacity)
    $('.detailphonecolor').text(phoneData.color)
    $('.detailphonedate').text(`上市日期：${phoneData.since}`)
    $('.detailcount').text(phoneData.click)
    $('.detailprice').text(phoneData.price)
	var priceList = "";
	for (let x in phoneData.deductItems)
	{
		if (x.indexOf('capname') !== -1) 
		{
			var priceKey = x.replace('name', '');
			priceList += "<div class='detailphoneprice'>" + phoneData.deductItems[x] + " 最高回收價 <span class='detailprice'>" + phoneData.deductItems[priceKey] + "</span></div>";
		}
	}
	$('#priceList').html(priceList);
}

function autofill(num){
    $('[name=IMEI]').val(`00${num}`)
    $('[name=name]').val(`00${num}`)
    $('[name=SSN]').val(`00${num}`)
    $('[name=email]').val(`00${num}@example.com`)
    $('[name=phonenum]').val(`00${num}`)
    // $('[name=phonecheck]').val('')
    // $('[name=bank]').val('127 桃園信用合作社')
    // onChange('[name=bank]');
    // $('[name=accName]').val(`00${num}`)
    // $('[name=acc]').val(`00${num}`)
    // $('[name=pickupMethod]').val('HOME')
    $('[name=city]').val('高雄市')
    onChange('[name=city]');
    $('[name=address]').val('101 example st.')
    // $('input[type=checkbox]')[0].checked=true
    $('[name=branch]').val('1270116 南崁分社')
    $('[name=area]').val('六龜區')
}
function onChange(ss1){
    var el=document.querySelector(ss1);
    var evt = document.createEvent("HTMLEvents");
    evt.initEvent("change", false, true);
    el.dispatchEvent(evt);
}
//---------------- add ----
function getFormData(css1){
    var data={}
    document.querySelectorAll(css1+' [name]')
    .forEach(function(el){
        var key=el.getAttribute('name');
        var val=el.value;
        // console.log(key,val);
        data[key]=val;
    });
    // console.log(data);
    return data;
}
function validphone(data){
    var val=data['phonecheck']
    if (val==''){
        var old=getCache('old');
        if (old && 'phonenum' in old){
            var pn=data['phonenum']
            if (pn) {
                if (pn==old.phonenum) {
                    return true;
                }
            }
        }
    } else {
        if (val==smssig) {
            return true;
        }
    }
    return false;
}
var chineseMap1={
    name:'真實姓名',
    SSN:'身份證字號',
    email:'電子信箱',
    phonenum:'手機號碼',
    bank:'銀行名稱',
    branch:'分行名稱',
    accName:'戶名',
    acc:'匯款帳號',
    pickupMethod:'收件方式',
    city:'縣市',
    area:'行政區',
    address:'地址',
    storearea:'門市地區',
    storename:'門市名稱',
    storeaddress:'門市地址',
}
function validate(hint,data){
    function fail(err){
        toast(err)
        return false;
    }
    function mustfill(key,data){
        var ch=chineseMap1[key]
        ch=ch?ch:key
        return fail(`必須填寫 ${ch}`);
    }
    var ok=validphone(data)
    // console.log(ok);
    if (!ok) {
        return fail('手機號碼未通過驗證');
    }
    if (data['pickupMethod']=='到府收件') {
        if (data['city']=='') {
            return mustfill('city');
        }
        if (data['area']=='') {
            return mustfill('area');
        }
        if (data['address']=='') {
            return mustfill('address');
        }
    }
    if (data['pickupMethod']=='⾨市收件') {
        if (data['storearea']=='') {
            return mustfill('storearea');
        }
        if (data['storename']=='') {
            return mustfill('storename');
        }
        if (data['storeaddress']=='') {
            return mustfill('storeaddress');
        }
    }
    var exempt='phonecheck,city,area,address,storearea,storename,storeaddress,storetel'
    if (location.pathname.indexOf('accountcenter.html')>-1) {
        exempt+=',bank,branch,accName,acc,birthdate,gender'
    }
    if (data['pickupMethod']=='⾨市收件') {
        exempt+='bank,branch,accName,acc'
    }
    exempt=exempt.split(',')
    for (var key of Object.keys(data)) {
        if (exempt.indexOf(key)>-1) {
            continue;
        }
        var val=data[key]
        if (val=='') {
            return mustfill(key);
        }
    }
    return true;
}
function today() {
    var dt=new Date()
    var y=dt.getFullYear();
    var m=dt.getMonth()+1;
    var d=dt.getDate();
    m=String(m).padStart(2,'0');
    d=String(d).padStart(2,'0');
    return `${y}-${m}-${d}`;
}
function clickOrder(cb){
    saveOrder(cb);
}
function sim2(){
    $('[name=IMEI]').val(Math.random())
    $('[type=checkbox]').prop('checked',true)
    $('button.wantsell').click()
}
function saveOrder(cb) {
    // $('input[name=IMEI]')[0].value='test123';
    var css1='.orderinfo'
    var data=getFormData(css1)
    var ok= validate('orders',data)
    if (ok) {
        // $('button.wantsell').prop('disabled',true)
        var alist=Object.keys(getCache('anslist'));
        var phoneinfo=getCache('phoneinfo')
        data['type']=phoneinfo.type;
        data['brand']=phoneinfo.brand;
        data['model']=phoneinfo.model;
        data['conditions']=alist.join()
        data['estAmounts']=getCache('est')
        data['regId']=getCache('regId')
        data['regMethod']=getCache('regMethod')
        data['modelId']=getCache('model.id')
        addRec('orders',data,function(s){
            console.log(s);
            var msg=JSON.parse(s)
            if (msg.error==undefined) {
                cb(msg) // showBigTick
                // addRecCB(msg)
                pubBell(msg)
                if (msg.isNew) {
                    confirmAction(msg,function() {
                            afterBigTick(msg)
                    })
                } else {
                    afterBigTick(msg)
                }
            } else {
                // $('button.wantsell').prop('disabled',false)
                toast('error 101')
            }
        });
    }
}
function afterBigTick(msg){
    location.href='estimaterecord.html'
    // console.log(msg);
    // msg=JSON.parse(msg)
    // if (msg.isNew) {
    //     $.get('register_success.html#s',function(out){});
    // }
    // location.href='buy_success.html'
}
const URLROOT=''
function listOther(tb,cb) {
    var url=URLROOT + 'other/'+tb;
    $.getJSON(url,null,function(rs){
        cb(rs,tb)
    });
}
function listRec(tb,cb) {
    var url=URLROOT + 'consumer/'+tb;
    var jsonobj = $.getJSON(url,null,function(rs){
		console.log("rs="+JSON.stringify(rs));
        cb(rs,tb)
    });
	
}
function getRec(tb,id,cb) {
    var url=URLROOT + 'consumer/'+tb+'/' + id;
    $.getJSON(url,null,function(row){
        cb(row)
    });
}
function addRec(tb,data,cb){
    // console.log('addRec:',tb,data);
    var url=URLROOT + 'consumer/'+tb;
    $.post(url,data,function(msg){
        cb(msg)
    });
}
function addRecCB(msg){
    // console.log('addRecCB:',msg);
    var data=JSON.parse(msg)
}
function updateRec(tb,id,data,cb){
    // console.log('updateRec:',tb,id,data);
    var url=URLROOT + 'mod/member/' + id;
    $.ajax({
       url: url,
       data: data,
       error: function(e) {
          console.log(e);
       },
       dataType: 'json',
       success: function(data) {
           cb(data)
       },
       type: 'PATCH'
    });
}
function clickcount(i){
    var c=sessionStorage.getItem('click')
    sessionStorage.removeItem('click')
    if (c) {
        $.getJSON('/consumer/clickcount/'+i);
    }
}
function onclickphone(i){
    // console.log(i);
    setCache('model.id',i);
    sessionStorage.setItem('click',1);
    window.location.href = "phoneinfo.html";
}
function utoa(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
}
function atou(str) {
    return decodeURIComponent(escape(window.atob(str)));
}
function addAns(item,check){
    var code = $(item).find('[code]').attr('code');
    var text = $(item).find('[code]').text();
    // console.log(code,check);
    if (check) {
        anslist[code]=1
        pickCapColor(code,text)
    } else {
        delete anslist[code]
    }
    setCache('anslist',anslist)
}

function pickCapColor(code,text) {
    if (isCap(code)) {
        setCache('capacity.text',text)
    }
    if (isColor(code)) {
        setCache('color.text',text)
    }
}
function estimate(cb){
    var anslist=getCache('anslist')
    var anslist=Object.keys(anslist)
    var id=getCache('model.id')
    var data={anslist:anslist,id:id}
    var url=URLROOT + 'consumer/estimate';
    $.post(url,data,function(msg){
        cb(msg)
    });
}
function fixChooselist(name,word){
    // console.log('fixChooselist:',name,word);
    if (word==null) {
        return;
    }
    var el=document.querySelector(`select[name=${name}]`);
    if (el){
        el.value=word;
        if (el.selectedIndex==-1) {
            el.innerHTML+=`<option val="${word}" selected>${word}</option>`;
        }
    }
}
function newmember(cb){
    var regId=getCache('regId')
    addMember(regId,cb);
}
function renderMember(mb){
    if (mb){
        setCache('old',mb)
        renderFormCB2(mb);
        $('[name=phonecheck]').val('')
        fixChooselist('bank',mb.bank)
        onbank(mb.bank)
        fixChooselist('branch',mb.branch)
        fixChooselist('city',mb.city)
        oncity(mb.city)
        fixChooselist('area',mb.area)
    }
}
function memberinfo(isAccountcenter=false){
    var regId=getCache('regId')
    getMember(regId,function(mb){
        if (mb) {
            renderMember(mb)
        } else {
            if (isAccountcenter) {
                toast('您還沒有完成註冊，請正確填寫會員資料，點擊『儲存』完成註冊。')
            }
        }
    });
}
function drawTable(a){
    TBupdate('#table1',a)
}
function mapShipStatus(s){
    if (!s) {
        return '尚未取得物流資訊'
    }
    return s;
}
function ordersinfo(state){
    var regId=getCache('regId');
    getRec('ordersfor',regId,function(a){
        a.sort((x,y)=>{ return x._updateAt > y._updateAt?-1:(x._updateAt < y._updateAt?1:0) })
        a=filterstate(a,state)
        a=a.map(o=>{
            if ('shipStatus' in o) {
                o.shipStatus=mapShipStatus(o.shipStatus)
            }
            if ('returnStatus' in o){
                o.returnStatus=mapShipStatus(o.returnStatus)
            }
            // o._action_= toolbox(eye(state,o.id))
            o._action_= `clickAction(event,'view','${state}',${o.id})`;
            return o;
        });
        switch (state){
            case 'NEW':
                a=screen(a,'_updateAt ordernum model estAmounts pickupMethod shipStatus _action_'); break;
            case 'SOLD':
                a=screen(a,'_updateAt ordernum model finalAmounts remitTime _action_'); break;
            case 'CANCEL':
                a=screen(a,'_updateAt ordernum model estAmounts returnStatus _action_');
                // a=screen(a,'ordernum _action_ model estAmounts returnStatus finalAmounts');
                // for (var i=0;i<a.length;i++){
                //     if (a[i].finalAmounts!=null) {
                //         a[i].estAmounts=a[i].finalAmounts
                //     }
                //     delete a[i]['finalAmounts']
                // }
            break;
        }
        var tmp=$('#tmp102').html()
        var b=renderTemplate(tmp,a)
        drawTable(b)
        if (state=='SOLD') {
            var total=0;
            if (a.length>0) {
                total=a.map(o=> +o.finalAmounts).reduce((a,b)=>a+b);
            }
            var s=dollar(total);
            var msg=`賣出總額：${s} 元`
            $('.totlesellprice').text(msg)
        }
    });
}
function filterstate(a,state){
    return a.filter(o=>{
        var boo=false;
        switch (o.status) {
            case 'NEW2':
                boo= state=='NEW';
            break;
            case 'SOLD2':
                boo= state=='SOLD';
            break;
            case 'NEW':
            case 'WAIT':
            case 'PENDING':
                boo= state=='NEW';
            break;
            case 'SOLD':
            case 'REMIT':
                boo= state=='SOLD';
                break;
            case 'CANCEL':
                boo= state=='CANCEL';
                break;
        }
        // console.log('filterstate:', o.ordernum, o.status,state,boo);
        return boo;
    })
}
function renderFormCB2(row){
    for (var key of Object.keys(row)) {
        var el=document.querySelector(`[name=${key}]`);
        if (el) {
            el.value=row[key];
            // console.log('found:',key,el.value);
        } else {
            // console.log('not found:',key);
        }
    }
}
//----------------------------------------
const Taiwan={
  "emptyTable": "無資料...",
  "processing": "處理中...",
  "loadingRecords": "載入中...",
  "lengthMenu": "顯示 _MENU_ 項結果",
  "zeroRecords": "沒有符合的結果",
  "info": "顯示第 _START_ 至 _END_ 項結果，共 _TOTAL_ 項",
  "infoEmpty": "顯示第 0 至 0 項結果，共 0 項",
  "infoFiltered": "(從 _MAX_ 項結果中過濾)",
  "infoPostFix": "",
  "search": "搜尋:",
  "paginate": {
    "first": "第一頁",
    "previous": "<",
    "next": ">",
    // "previous": "上一頁",
    // "next": "下一頁",
    "last": "最後一頁"
  },
  "aria": {
    "sortAscending": ": 升冪排列",
    "sortDescending": ": 降冪排列"
  }
};
function TBupdate(css,rs){
    var array = flatten(rs);
    var targets=[]
    if (array.length>0) {
        var r0=array[0];
        var cols=r0.length-1;
        var tg=[]
        for (var i=0;i<cols;i++){
            tg.push(i)
        }
        targets=tg;
    }
    var table;
    if (document.querySelector(css+'.dataTable')==null){
        document.querySelector('table thead tr').removeAttribute('hidden');
        table=$(css).DataTable({
            data:array,
            language:Taiwan,
            order: [[ 0, "desc" ]],
            pageLength:5,
            ordering:false,
            columnDefs: [
                {
                    "targets": targets,
                    "visible": false
                }
            ],
            info:     false,
            lengthChange:false,
            drawCallback:renderBlob
        });
        // var el;
        // el=document.querySelector('.paginate_button.current')
        // el.setAttribute('class','my_current_pager');
        // $('.paginate_button.previous').css({content:"url(../image/left.png)"})
        // $('.paginate_button.next'    ).css({content:"url(../image/right.png)"})
        // el.setAttribute('class','pg-prev');
        // el=document.querySelector('.paginate_button.next')
        // el.setAttribute('class','pg-next');
        // table.on('draw',function(){
        //    // console.log('completedd');
        // })
    } else {
        // table=$(css).DataTable();
        // table.clear()
        // table.rows.add(array)
        // table.draw()
    }
}
function flatten(rs){
    var a=[]
    for (var row of rs) {
        var item=Object.values(row)
        a.push(item)
    }
    return a
}
function toolbox(tools){
    return `<div class="toolbox">${tools}</div>`
}
function eye(name,id){
    return `<a href='javascript:void(0)' onclick="clickAction(event,'view','${name}',${id})">訂單明細</a>`
}
function screen(a,whitelist) {
    if (a==null){
        return null;
    }
    var b=[]
    whitelist=whitelist.split(' ')
    for (var item of a){
        var o={}
        for (var k of whitelist) {
            o[k]=item[k]
        }
        b.push(o)
    }
    return b;
}
function toast(msg) {
  var el = document.getElementById("snackbar");
  if (!el){
      $('body').append('<div id="snackbar"></div>')
  }
  el=document.getElementById("snackbar");
  el.className = "show";
  el.innerHTML=msg;
  setTimeout(function(){ el.className = el.className.replace("show", ""); }, 3000);
}
function isCap(code){
    var reg1=/^cap\d+$/
    return reg1.test(code);
}
function isColor(code){
    var reg1=/^color\d+$/
    return reg1.test(code);
}
function checkAns(){
    var has_cap=false;
    var has_color=false;
    var anslist=getCache('anslist')
    if (anslist){
        for (var code of Object.keys(anslist)) {
            if (isCap(code)) {
                has_cap=true;
            }
            if (isColor(code)) {
                has_color=true;
            }
        }
    }
    if (!(has_cap && has_color)){
    // if (true) {
        toast('必選容量和顏色') //提醒您：
        return false;
    }
    window.location.href = "phoneprice.html";
    return true;
}
// clickAction(event,'view','NEW',7)
function clickAction(e,action,state,id){
    setCache('oid',id)
    switch (state){
        case 'NEW': location.href='estimateinfo.html'; break;
        case 'SOLD': location.href='sellinfo.html'; break;
        case 'CANCEL': location.href='cancelinfo.html'; break;
    }
}
function renderDIV(o){
    document.querySelectorAll('[name]').forEach((el,i)=>{
        var key=el.getAttribute('name');
        var val=o[key]
        switch(el.tagName){
            case 'DIV':
                el.innerText='';
                el.innerText=val;
                break;
            case 'IMG':
                if (val) {
                    el.src=val;
                }
                break;
        }

    });
}
function phoneinfoCB(order){
    return function(phone){
        setCache('phoneinfo',phone)
        var testitems=phone.details.testitems;
        var flatlist=order.conditions
        var anslist={}
        if (typeof(flatlist)=='string' && flatlist.length>0) {
            for (var word of flatlist.split(',')){
                anslist[word]=1
            }
        }
        // console.log(testitems,anslist);
        drawOrder(testitems,anslist)
    }
}
function orderCB(o){
    if (!o.finalAmounts) {
        o.finalAmounts=o.estAmounts
    }
    if ('shipnum' in o){
        o.shipnum=mapShipStatus(o.shipnum)
    }
    if ('returnnum' in o){
        o.returnnum=mapShipStatus(o.returnnum)
    }
    renderDIV(o)
    $('select[name=pickupMethod]:eq(0)').val(o.pickupMethod)
    var mid=o.modelId;
    getRec('phonelist',mid,phoneinfoCB(o))
    if ($('[name=shipStatus]').length>0) {
        $('[name=shipStatus]').load('track.html',function(out){
            var shipnum=$('[name=shipnum]').text()
            track(shipnum)
        })
    }
    if ($('[name=returnStatus]').length>0) {
        $('[name=returnStatus]').hide()
        $('[name=returnStatus]').load('track.html',function(out){
            var shipnum=$('[name=returnnum]').text()
            track(shipnum)
            $('[name=returnStatus]').show()
        })
    }
    if ($('[name=pickupMethod]:eq(0)').val()=='到府收件') {
        $('.informationline4.p1').show()
        $('.informationline4.p2').hide()
    } else {
        $('.informationline4.p1').hide()
        $('.informationline4.p2').show()
    }
    setTimeout(function (){
        if ($('[name=pickupMethod]:eq(0)').text()=='到府收件') {
            // $('[name=shipnum]').text('派車到府收件')
            $('.time-line-message').text('派車到府收件')
        } else {
            // $('[name=shipnum]').text('門市預約回收')
            $('.time-line-message').text('門市預約回收')
        }
    },500);
}
function showOrder(state,cb=orderCB) {
    var oid=getCache('oid')
    // deCache('oid')
    getRec('orders',oid,cb)
}
function onLoginFail(){
    setFlash('loginfail') //登錄失敗,請勾選電子郵件
    // console.log('login failed...would go back...not for now');
    if (swal2_timer){
        clearTimeout(swal2_timer)
        swal2_timer=null;
    }
    location.reload()
    return;
    var prev=getCache('prev')
    if (prev) {
        deCache('prev')
        deCache('next')
        window.location.href=prev;
    }
}
const nextmap={
    'wantsell wantsell2':"order.html",
    account:"accountcenter.html"
}
function onSocial(msg) {
    var msg=JSON.parse(msg);
    var regId=msg['regId'];
    var method=msg['regMethod'];
    var disabled=msg['disabled']==1;
    deCache('prev')
    if (disabled) {
        if ($('.logintext')[0]) {
            $('.logintext').css('visibility','hidden')
            $('.loginbuttonarea').css('visibility','hidden')
            $('.bigtitletext2').text('此帳號已經停用！')
        } else {
            location.href='account_disabled.html'
        }
    } else {
        setCache('regMethod',method);
        setCache('regId',regId);
        goNext()
    }
}
// function handlesuccess(o,cb) {
//     var q=btoa(encodeURIComponent(JSON.stringify(o)));
//     $.post('/other/handlesuccess',{q:q},cb);
// }
// function onLoginSuccess(method,info,email) {
//     handlesuccess({method:method,info:info,email:email},function(msg){
//         var msg=JSON.parse(msg);
//         var regId=msg['regId'];
//         var method=msg['regMethod'];
//         var disabled=msg['disabled']==1;
//         deCache('prev')
//         if (disabled) {
//             if ($('.logintext')[0]) {
//                 $('.logintext').css('visibility','hidden')
//                 $('.loginbuttonarea').css('visibility','hidden')
//                 $('.bigtitletext2').text('此帳號已經停用！')
//             } else {
//                 location.href='account_disabled.html'
//             }
//         } else {
//             setCache('regMethod',method);
//             setCache('regId',regId);
//             goNext()
//         }
//     })
// }
function isMemberEnabled(regId,cb) {
    var url=URLROOT + 'other/member/enabled';
    var data={
        regId:regId
    }
    $.post(url,data,function(data){
        var o=JSON.parse(data)
        cb(o);
    })
}
function getMember(regId,cb) {
    var url=URLROOT + 'other/member/get';
    var data={
        regId:regId
    }
    $.post(url,data,function(data){
        var o=JSON.parse(data)
        cb(o);
    })
}
function addMember(regId,cb) {
    var url=URLROOT + 'consumer/member';
    var data={
        regId:regId,
    }
    $.post(url,data,function(data){
        var o=JSON.parse(data)
        cb(o);
    })
}
function setFlash(msg){
    setCache('flash',msg)
}

function initlogin() {
    $('button.wantsell2').attr('onclick',"proceed(event,1)")
    $('img.account').attr('onclick',"proceed(event,2)")
}
initlogin()
function proceed(e,i){
    setCache('nexti',i);
    showlogin(e)
}
function goNext() {
    var nextmapi=['index','order','accountcenter','sellinfo','cancelinfo','estimateinfo']
    var i=getCache('nexti')
    deCache('nexti')
    if (i==null) { return; }
    i= (i<0 || i>6)?0:i
    var p = nextmapi[i];
    location.href= `${p}.html`
}
function showlogin(e){
    if (e){
        e.preventDefault()
        e.stopPropagation()
    }
    var regId=getCache('regId');
    if (regId) {
        isMemberEnabled(regId,function(msg){
            if (msg.enabled==1){
                goNext()
            } else {
                deCache('regId')
                doDialog()
            }
        })
    } else {
        doDialog()
    }
    function doDialog() {
        setCache('prev',location.href);
        $('#loginplacehold').remove();
        $('body').append('<div id="loginplacehold"></div>')
        $('#loginplacehold').load('loginpanel.html',function(out){
            showlogin2();
        });
    }
}
var smssig=null;
var smsexpire=0;
function sms(dst) {
    smssig=null;
    var url='sms.php';
    var data={dst:dst}
    poster(url,data,function(out){
        try {
            var a=out.split('\n');
            smssig=a[0]
            smsexpire=a[1]

        } catch(e) {}
    });
}
function smsverify(cmsg,code) {
    return (Date.now()/1000)<smsexpire&&cmsg==code?1:0
}
function isDigitsOnly(num){
    re=/^\d+$/;
    return re.test(num)
}
function sendnumber(e){
    e.preventDefault()
    e.stopPropagation()
    var num=document.querySelector('input[name=phonenum]').value;
    if (!isDigitsOnly(num)) {
        toast('只接受數字為手機號碼')
        return;
    }
    isUniqueNumber(num,function(msg){
        if (msg.uniq) {
            sms(num);
            toast(`已發送簡訊至 ${num}`)
        } else {
            toast(`此號碼已經使用 "${msg.sop}” 註冊為會員,無法重覆註冊`)
        }
    })
}
function isUniqueNumber(num,cb) {
    getRec('uniqnumber',num,cb)
}
function verifynumber(){
    var code=document.querySelector('input[name=phonecheck]').value;
    if (smsverify(smssig,code)) {
        document.querySelector('input[name=phonenum]').disabled=true;
        document.querySelector('button.sendnumber').disabled=true;
        document.querySelector('input[name=phonenum]').style.backgroundColor='lime';
        return true;
    }
    return false;
}
function phonelist(cb,type,brand,q,off,limit=16,precise=false,hot=false){
    // console.log(type,q,off,limit);
    var params=[]
    if (type) {
        params.push('type='+type)
    }
    if (brand) {
        brand=brand.trim()
        params.push('brand='+encodeURIComponent(brand))
    }
    if (q) {
        q=q.trim()
        params.push('q='+encodeURIComponent(q))
    }
    if (off) {
        params.push('off='+off)
    }
    if (limit) {
        params.push('limit='+limit)
    }
    if (precise) {
        params.push('precise=1')
    }
    if (hot) {
        params.push('hot=1')
    }
    var s=params.join('&')
    if (s.length>0) {
        s = '?'+s
    }
    var url='phonelist2' + s;
    listRec(url,cb);
}
function getSearchText(){
    var n=$('[name=searchtext]').length;
    for (var i=0;i<n;i++){
        var o=$('[name=searchtext]')[i];
        if (o.offsetParent) {
            var text=o.value;
            o.value='' // cleanup
            return text;
        }
    }
    return ''
}
function renderPricehistory(mid){
    function renderChart(a){
        var labels=[]
        var data=[]
        for (var o of a){
            labels.push(o.date)
            data.push(o.price)
        }
        drawChart(labels,data)
    }
    listOther('pricehistory/'+mid,function(a){
        renderChart(a)
    })
}
function searchModel(name){
    var url='/consumer/modelIdByName'
    $.post(url,{name:name},function(i){
        onclickphone(i)
    })
}
function hotSearch(e){
    e.preventDefault()
    e.stopPropagation()
    var name=e.target.innerText
    searchModel(name)
}
function isPrefix(pattern,word){
    var patt='^' + pattern + '\\d+$';
    return (new RegExp(patt)).test(word)
}
function isCapColor(code){
    return isPrefix('cap',code)||isPrefix('color',code)
}
function protect(){
    var boo=getCache('regId')!=null;
    if (!boo) {
        location.href='index.html'
    }
    return boo;
}
var skipdelta=false;
function deltaOnly(old,data){
    if (skipdelta) {
        skipdelta=false;
        return data;
    }
    var o={}
    for (var k of Object.keys(data)){
        if (k in old) {
            // console.log('k=',k);
            var v=old[k]
            var v2=data[k]
            if (v!=v2){
                o[k]=v2
            }
        }
    }
    // console.log('delta:',o);
    return o;
}
function saveMember(e) {
    if (e) {
        e.preventDefault()
        e.stopPropagation()
    }
    function savemember1(data,cb){
        $.post('/other/savemember',data,cb);
    }
    var data=getFormData('.accountcenterinformation');
    data.regId=getCache('regId');
    data.regMethod=getCache('regMethod');
    var id=data.id
    if (!data.id) {
        delete data.id;
    }
    var ok= validate('member',data)
    if (ok) {
        if (id) {
            savemember1(data,function(out){
                if (out.error==undefined) {
                    saveMemberCB()
                } else {
                    toast('error 101');
                }
            });
        } else {
            savemember1(data, function(out){
                if (out.error==undefined) {
                    confirmAction(out,function(){
                        location.href='register_success.html' // showBigTick too!
                        // toast('註冊成功!');
                    });
                } else {
                    toast('error 101');
                }
            });
        }
    }
}
// function updateMemberCB(msg){
//     // console.log('update member cb:',msg);
//     saveMemberCB()
//     // setTimeout(()=>{
//     //     location.href='index.html'
//     // },1800)
// }
// function updateMember(e,cb=updateMemberCB){
//     var data=getFormData('.accountcenterinformation');
//     var id=data.id
//     if (!id) {
//         // console.log('ERROR: no id!');
//         delete data.id;
//         var ok= validate('member',data)
//         if (ok) {
//             newmember(function(id){
//                 // console.log(id);
//                 if (parseInt(id)>0){
//                     $('input[name=id]').val(id);
//                     skipdelta=true;
//                     updateMember(e,function(msg){
//                         toast('註冊成功!');
//                         setTimeout(function(){
//                             location.href='register_success.html'
//                         },4000);
//                     });
//                 }
//             })
//         }
//         return;
//     }
//     const name='member';
//     var ok= validate(name,data)
//     if (ok) {
//         var old=getCache('old')
//         data = deltaOnly(old,data)
//         // console.log('DELTA:', data);
//         updateRec(name,id,data,cb);
//     }
// }
function restoreMember(e){
    location.href='index.html'
    // var old=getCache('old')
    // renderMember(old)
}
function initLogout() {
    var el=document.querySelector('.logout');
    if (el) {
        el.setAttribute('onclick',"logout(event)");
    }
}
initLogout()
function logout() {
    deCacheAll()
    location.href='index.html'
}
function autoload(name) {
    if (document.querySelector(`select[name=${name}]`)) {
        $('body').append(`<script id="${name}sc" src="jsmain/${name}.js"></script>`)
    }
}
autoload('city')
autoload('bank')
function gosearch2(isLocal=false){       // only good for search on phonelist.html
    var text=getSearchText();
    setCache('modelFilter',text)
    if ($('.chooseoptiontext2')[0]){
        var brandFilter = $('.chooseoptiontext2')[0].innerText
        setCache('brandFilter',brandFilter)
    }
    if ($('.chooseoptiontext2')[1]){
        var typeFilter = $('.chooseoptiontext2')[1].innerText
        setCache('typeFilter',typeFilter)
    }
    if (isLocal) {
        gosearch3()
        return;
    }
    location.href='searchresult.html'
}
function keyEnterSearch(e){
    if (e.keyCode === 13) {
        e.preventDefault();
        var btn1=e.target.parentNode.parentNode.querySelector('a.gosearch')
        var btn2=e.target.parentNode.parentNode.querySelector('button.gosearch2')
        var btn=btn1?btn1:(btn2?btn2:null);
        if (btn){
            btn.click()
        }
    }
}
function renderTemplate(tmp,a){
    // var b=[]
    for (var row of a) {
        var ts=row._updateAt;
        delete row._updateAt;
        // console.log(row);
        var tmp1=String(tmp);
        for (var k of Object.keys(row)) {
            var key=new RegExp('@'+k,'g');
            tmp1=tmp1.replace(key,row[k])
        }
        delete row._action_
        var blob=utoa(tmp1)
        row['tmp']=`<div blob="${blob}">?</div>`;
    }
    // console.log(a);
    return a;
}
function renderBlob(){
    $('#table1').width('100%').css('border-bottom-color','white')
    document.querySelectorAll('[blob]').forEach(function(el){
        var blob=el.getAttribute('blob')
        var frag=atou(blob)
        el.innerHTML=frag;
        // console.log(frag);
    })
}
function pubBell(msg){
    // msg=JSON.parse(msg)
    mpub(String(msg['storepickup']));
}
function loadContract(i){
    $('.contract').load(`/contract/contract${i}.html`);
}
function window_open(e,link){
    e.preventDefault()
    e.stopPropagation()
    if (link && typeof(link)=='string' && link.length>0) {
        window.open(link,'_blank');
    }
}
function bh(s) {
  var o=btoa(s)
  var k=md5(o)
  return o+'.'+k
}
function hb(ok) {
  if (ok==null) { return null }
  [o,m]=ok.split('.')
  var m0=md5(o)
  if (m0!=m) { return null }
  return atob(o);
}
!function(n){"use strict";function d(n,t){var r=(65535&n)+(65535&t);return(n>>16)+(t>>16)+(r>>16)<<16|65535&r}function f(n,t,r,e,o,u){return d((c=d(d(t,n),d(e,u)))<<(f=o)|c>>>32-f,r);var c,f}function l(n,t,r,e,o,u,c){return f(t&r|~t&e,n,t,o,u,c)}function v(n,t,r,e,o,u,c){return f(t&e|r&~e,n,t,o,u,c)}function g(n,t,r,e,o,u,c){return f(t^r^e,n,t,o,u,c)}function m(n,t,r,e,o,u,c){return f(r^(t|~e),n,t,o,u,c)}function i(n,t){var r,e,o,u;n[t>>5]|=128<<t%32,n[14+(t+64>>>9<<4)]=t;for(var c=1732584193,f=-271733879,i=-1732584194,a=271733878,h=0;h<n.length;h+=16)c=l(r=c,e=f,o=i,u=a,n[h],7,-680876936),a=l(a,c,f,i,n[h+1],12,-389564586),i=l(i,a,c,f,n[h+2],17,606105819),f=l(f,i,a,c,n[h+3],22,-1044525330),c=l(c,f,i,a,n[h+4],7,-176418897),a=l(a,c,f,i,n[h+5],12,1200080426),i=l(i,a,c,f,n[h+6],17,-1473231341),f=l(f,i,a,c,n[h+7],22,-45705983),c=l(c,f,i,a,n[h+8],7,1770035416),a=l(a,c,f,i,n[h+9],12,-1958414417),i=l(i,a,c,f,n[h+10],17,-42063),f=l(f,i,a,c,n[h+11],22,-1990404162),c=l(c,f,i,a,n[h+12],7,1804603682),a=l(a,c,f,i,n[h+13],12,-40341101),i=l(i,a,c,f,n[h+14],17,-1502002290),c=v(c,f=l(f,i,a,c,n[h+15],22,1236535329),i,a,n[h+1],5,-165796510),a=v(a,c,f,i,n[h+6],9,-1069501632),i=v(i,a,c,f,n[h+11],14,643717713),f=v(f,i,a,c,n[h],20,-373897302),c=v(c,f,i,a,n[h+5],5,-701558691),a=v(a,c,f,i,n[h+10],9,38016083),i=v(i,a,c,f,n[h+15],14,-660478335),f=v(f,i,a,c,n[h+4],20,-405537848),c=v(c,f,i,a,n[h+9],5,568446438),a=v(a,c,f,i,n[h+14],9,-1019803690),i=v(i,a,c,f,n[h+3],14,-187363961),f=v(f,i,a,c,n[h+8],20,1163531501),c=v(c,f,i,a,n[h+13],5,-1444681467),a=v(a,c,f,i,n[h+2],9,-51403784),i=v(i,a,c,f,n[h+7],14,1735328473),c=g(c,f=v(f,i,a,c,n[h+12],20,-1926607734),i,a,n[h+5],4,-378558),a=g(a,c,f,i,n[h+8],11,-2022574463),i=g(i,a,c,f,n[h+11],16,1839030562),f=g(f,i,a,c,n[h+14],23,-35309556),c=g(c,f,i,a,n[h+1],4,-1530992060),a=g(a,c,f,i,n[h+4],11,1272893353),i=g(i,a,c,f,n[h+7],16,-155497632),f=g(f,i,a,c,n[h+10],23,-1094730640),c=g(c,f,i,a,n[h+13],4,681279174),a=g(a,c,f,i,n[h],11,-358537222),i=g(i,a,c,f,n[h+3],16,-722521979),f=g(f,i,a,c,n[h+6],23,76029189),c=g(c,f,i,a,n[h+9],4,-640364487),a=g(a,c,f,i,n[h+12],11,-421815835),i=g(i,a,c,f,n[h+15],16,530742520),c=m(c,f=g(f,i,a,c,n[h+2],23,-995338651),i,a,n[h],6,-198630844),a=m(a,c,f,i,n[h+7],10,1126891415),i=m(i,a,c,f,n[h+14],15,-1416354905),f=m(f,i,a,c,n[h+5],21,-57434055),c=m(c,f,i,a,n[h+12],6,1700485571),a=m(a,c,f,i,n[h+3],10,-1894986606),i=m(i,a,c,f,n[h+10],15,-1051523),f=m(f,i,a,c,n[h+1],21,-2054922799),c=m(c,f,i,a,n[h+8],6,1873313359),a=m(a,c,f,i,n[h+15],10,-30611744),i=m(i,a,c,f,n[h+6],15,-1560198380),f=m(f,i,a,c,n[h+13],21,1309151649),c=m(c,f,i,a,n[h+4],6,-145523070),a=m(a,c,f,i,n[h+11],10,-1120210379),i=m(i,a,c,f,n[h+2],15,718787259),f=m(f,i,a,c,n[h+9],21,-343485551),c=d(c,r),f=d(f,e),i=d(i,o),a=d(a,u);return[c,f,i,a]}function a(n){for(var t="",r=32*n.length,e=0;e<r;e+=8)t+=String.fromCharCode(n[e>>5]>>>e%32&255);return t}function h(n){var t=[];for(t[(n.length>>2)-1]=void 0,e=0;e<t.length;e+=1)t[e]=0;for(var r=8*n.length,e=0;e<r;e+=8)t[e>>5]|=(255&n.charCodeAt(e/8))<<e%32;return t}function e(n){for(var t,r="0123456789abcdef",e="",o=0;o<n.length;o+=1)t=n.charCodeAt(o),e+=r.charAt(t>>>4&15)+r.charAt(15&t);return e}function r(n){return unescape(encodeURIComponent(n))}function o(n){return a(i(h(t=r(n)),8*t.length));var t}function u(n,t){return function(n,t){var r,e,o=h(n),u=[],c=[];for(u[15]=c[15]=void 0,16<o.length&&(o=i(o,8*n.length)),r=0;r<16;r+=1)u[r]=909522486^o[r],c[r]=1549556828^o[r];return e=i(u.concat(h(t)),512+8*t.length),a(i(c.concat(e),640))}(r(n),r(t))}function t(n,t,r){return t?r?u(t,n):e(u(t,n)):r?o(n):e(o(n))}"function"==typeof define&&define.amd?define(function(){return t}):"object"==typeof module&&module.exports?module.exports=t:n.md5=t}(this);
function care(i,oid){
    setCache('oid',oid)
    proceed(null,i);
}
function confirmAction(msg,cb){
    if (typeof(msg)=='string') {
        msg=JSON.parse(msg)
    }
    // console.log('confirmAction:', msg);
    var xid=0;
    if (msg.memberId) {
        xid=msg.memberId
    }
    if (msg.uid && msg.uid>0) {
        xid=msg.uid
    }
    if (xid<=0) {
        return;
    }
    msg={num:1,xid:xid}
    $.post('/confirmAction.php',msg,function(out){
        // console.log(out);
        if (cb){
            cb(out)
        }
    })
}
function confirmAction2(num,xid,cb=null) {
    msg={num:num,xid:xid}
    $.post('/confirmAction.php',msg,function(out){
        // console.log(out);
        if (cb){
            cb(out)
        }
    })
}
function hito(){
    var id=getCache('model.hit')
    deCache('model.hit')
    var cap=getCache('capacity.text')
    if (id) {
        $.post('/consumer/hit/'+id,{cap:cap});
    }
}
function setupHito(){
    var id=getCache('model.id');
    setCache('model.hit',id)
}
function changePickupMethod(pickup){
    if (pickup=='到府收件') {
        $('.homepickup').show()
        $('.storepickup').hide()
    }
    if (pickup=='⾨市收件') {
        $('.homepickup').hide()
        $('.storepickup').show()
        fill_storearea(fill_store)
    }
}
function fill_storearea(cb){
    listOther('fill_storearea',function(a){
        var s=''
        for (var o of a) {
            var name=o['storearea']
            s+=`<option>${name}</option>`
        }
        $('select[name=storearea]').html(s)
        if (cb) {
            cb();
        }
    })
}
function fill_store(storearea){
    if (!storearea) {
        storearea=$('select[name=storearea]').val()
    }
    listOther('fill_store/'+storearea,function(a){
        var s=''
        var addr=''
        var tel=''
        for (var o of a) {
            if (s==''){
                addr=o['address']
                tel=o['tel']
            }
            var name=o['name']
            s+=`<option>${name}</option>`
        }
        $('select[name=storename]').html(s)
        $('input[name=storeaddress]').val(addr);
        $('input[name=storetel]').val(tel);
    })
}
function fill_storeaddress(){
    var storearea=$('select[name=storearea]').val()
    var store=$('select[name=storename]').val()
    listOther(`fill_storeaddress/${storearea}/${store}`,function(a){
        $('input[name=storeaddress]').val(a[0]['address']);
        $('input[name=storetel]').val(a[0]['tel']);
    })
}
var FAQ=`
<div class="inner"><a class="footertext" href="/hmenu.html?q=FAQ" target="_blank">舊機常見問題</a></div>
<div class="inner"><a class="footertext" href="/hmenu.html?q=FAQ" target="_blank">如何收貨？</a></div>
<div class="inner"><a class="footertext" href="/hmenu.html?q=FAQ" target="_blank">匯款相關詢問</a></div>
<div class="inner"><a class="footertext" href="/hmenu.html?q=FAQ" target="_blank">回收商品如何包裝？</a></div>
<div class="inner"><a class="footertext" href="/policy.html" target="_blank">隱私權政策</a></div>
<div class="inner"><a class="footertext" href="/recycling.html" target="_blank">回收聲明書</a></div>`
async function loadWebParts(){
    $.getJSON('/other/site/web',function(msg){
        if (msg) {
            renderMeta(msg.form)
            renderHeader()
            if ($('.allinnerfooter')[0]){
                $('.allinnerfooter .line:nth-of-type(1) div:nth-child(3)').html(msg.form.about)
                $('.allinnerfooter .line:nth-of-type(2) div:nth-child(3)').html(FAQ)
            }
            renderContactUs(msg.form)
            renderStoreMaps()
        }
    });
}
function renderMeta(o){
    $('title').text(o.title)
    $('meta[name=keywords]').attr('content',o.keywords)
    $('meta[name="description"]').attr('content',o.intro)
    $('meta[property="og:description"]').attr('content',o.intro)
    $('meta[property="og:image"]').attr('content',o.photo)
    $('meta[property="og:description"]').after(`<meta property="og:keywords" content="${o.keywords}">`)
    $('meta[name="description"]').after(`<meta name="image" content="${o.photo}">`)
}
function renderContactUs(o){
    // console.log(o);
    var htel= o.tel.startsWith('0')? o.tel.substr(1): o.tel
    if ($('.allinnerfooter')[0]) {
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[0].href=`tel:+886-` + htel
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[0].innerText=o.tel
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[1].href=o.lineurl
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[1].innerText=o.line
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[2].href=o.fburl
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[2].innerText=o.fb
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[3].href=o.emailurl
        $('.allinnerfooter .line:nth-of-type(4) .footertext a')[3].innerText=o.email
        $('.allinnerfooter .line:nth-of-type(4) .footertext')[4].innerText=o.lineinfo
    }
}
function renderStoreMaps(){
    if ($('.allinnerfooter')[0]) {
        listRec('stores/name',function(a){
            var i=0;
            var even=a.length<=5?5:Math.ceil(a.length/2)
            var s=''
            for (var o of a) {
                var href=`https://www.google.com/maps/search/創宇通訊${o.name}`
                s+=`<a href="${href}" class="footertext" target="_blank">${o.name}</a>`
                i++;
                if ((i%even)==0) {
                    s+='</div><div class="inner">'
                }
            }
            s=`<div class="inner">${s}</div>`
            $('.allinnerfooter .line:nth-of-type(3) div:nth-child(3)').html(s)
        })
    }
}
function renderHeader(){
    $.getJSON('/other/site/hmenu',function(a){
        // console.log(a);
        if ($('.headerleft')[0]) {
            for (var o of a) {
                if (o.active) {
                    var tag=`<a href="${o.link}" class="headertext" target="_blank">${o.name}</a>`
                    var tag2=`<a href="${o.link}" class="menutext">${o.name}</a>`
                    $('.headerleft').append(tag)
                    $('.menulistbg').append(tag2)
                }
            }
        }
    })
}
async function loadStores(){
    $('body').append('<div id="tmp_shoparea"></div>')
    $('#tmp_shoparea').load('shoparea.html',function(){
        drawShoparea()
    })
}
loadStores()
loadWebParts()

function changePickupMethod2(pickupMethod){
    if (pickupMethod=='到府收件') {
        $('#modal_box .p1').show()
        $('#modal_box .p2').hide()
        $('#modal_box .p3').show()
        $('#modal_box [name=status]').val('NEW')
        $('#modal_box [name=shipStatus]').val('派車到府收件')
        var city=$('#modal_box [name=city]').val()
        oncity(city)
        var bank=$('#modal_box [name=bank]').val()
        onbank(bank)
    } else {
        $('#modal_box .p1').hide()
        $('#modal_box .p2').show()
        $('#modal_box .p3').hide()
        $('#modal_box [name=status]').val('NEW2')
        $('#modal_box [name=shipStatus]').val('門市預約回收')
        fill_storearea(function (data){
            console.log(data);
            var storearea=$('#modal_box [name=storearea]').val()
            fill_store(storearea)
        })
    }
}
function isShipnum(s) {
    var reg = /^\d+$/;
    return reg.test(s)
}
function loadOrderbox(o){
    changePickupMethod2(o.pickupMethod)
    $('#modal_box [name=city]').val(o.city)
    $('#modal_box [name=area]').val(o.area)
    $('#modal_box [name=address]').val(o.address)
    $('#modal_box [name=storearea]').val(o.storearea)
    $('#modal_box [name=storename]').val(o.storename)
    $('#modal_box [name=storeaddress]').val(o.storeaddress)
    $('#modal_box [name=bank]').val(o.bank)
    $('#modal_box [name=branch]').val(o.branch)
    $('#modal_box [name=accName]').val(o.accName)
    $('#modal_box [name=acc]').val(o.acc)
    $('#modal_box [name=pickupMethod]').val(o.pickupMethod)
    if (isShipnum(o.shipnum)) {
        $('.changeaddress').unbind()  // only editable when shipnum is not null!
    }
    oncity(o.city)
    $('#modal_box [name=area]').val(o.area)
    onbank(o.bank)
    $('#modal_box [name=branch]').val(o.branch)
    if (o.pickupMethod=='⾨市收件') {
        $('.p3').hide()
    } else {
        $('.p3').show()
    }
    $('#modal_box [name=shipStatus]').val(o.shipStatus)
}
function cancelOrderBox(){
    if (confirm('是否要取消本次回收訂單？ (點擊確認取消訂單)')) {
        var id=$('[name=id]').text()
        $.post('/other/cancelOrders/'+id,{},function(out){
            $('#modal_box').hide()
            confirmAction2(7,id)
            location.href='cancelrecord.html'
        })
    }
}
function updateOrderBox(){
    var data;
    var id=$('[name=id]').text()
    var method=$('#modal_box [name=pickupMethod]').val()
    if (method=='到府收件') {
        var bank=$('#modal_box [name=bank]').val()
        var branch=$('#modal_box [name=branch]').val()
        var accName=$('#modal_box [name=accName]').val()
        var acc=$('#modal_box [name=acc]').val()
        if (bank=='') {
            toast('銀行名稱 必填');
            return;
        }
        if (branch=='' || branch==null) {
            toast('分行名稱 必填');
            return;
        }
        if (accName=='') {
            toast('戶名 必填');
            return;
        }
        if (acc=='') {
            toast('匯款帳號 必填');
            return;
        }
        var city=$('#modal_box [name=city]').val()
        var area=$('#modal_box [name=area]').val()
        var address=$('#modal_box [name=address]').val()
        data={
            pickupMethod:method,
            city:city,
            area:area,
            address:address,
            bank:bank,
            branch:branch,
            accName:accName,
            acc:acc
        }
    } else {
        var storename=$('#modal_box [name=storename]').val()
        var storearea=$('#modal_box [name=storearea]').val()
        var storeaddress=$('#modal_box [name=storeaddress]').val()
        data={
            pickupMethod:method,
            storename:storename,
            storearea:storearea,
            storeaddress:storeaddress
        }
    }
    var status=$('[name=status]').val();
    if (status=='NEW'||status=='NEW2') {
        data['status']=status
    }
    data['shipStatus']=$('#modal_box [name=shipStatus]').val()
    if (confirm('是否要變更本訂單收件方式？')) {
        $.post('/other/updateOrders/'+id,data,function(out){
            $('#modal_box').hide()
            confirmAction2(8,id)
            location.reload()
        })
    }
}
