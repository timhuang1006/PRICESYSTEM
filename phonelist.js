var label = ["全部","蘋果","HTC","LG","ASUS","Google","小米","VIVO","三星"];
var model = ["全部","手機","平板"];

var labelclickitem;
var modelclickitem;

function draw2e() {
    if (location.hash=='') {
        draw2()
    } else {
        draw2()
        setTimeout(function(){
            // setCache('brandFilter',location.hash.substr(1))
            // draw2d(0)
            var brand=location.hash.substr(1)
            $('#labellist>div').each((i,el)=>{
                var text=el.innerText
                if (text==decodeURIComponent(brand)) {
                    $(el).click()
                }
            })
        },500)
    }
}
function draw2(brand='') {
    deCache('modelFilter')
    deCache('brandFilter')
    deCache('typeFilter')
    if (brand!='') {
        setCache('brandFilter',brand)
    }
    listRec('allbrands',function(a){
        var b=a.map(o=>o.brand)
        // console.log(b);
        b.unshift("全部");
        draw2a(b);
        draw2b(model);
        setFilter()
    })
}
function draw2d(off=0){
    var brand=null;
    var type=null;
    var q='';
    q=getCache('modelFilter')
    brand=getCache('brandFilter')
    type=getCache('typeFilter')
    if (brand=='全部') {
        brand=null;
    }
    if (type=='全部') {
        type=null;
    }
    if (q=='') {
        q=null
    }
    function drawph0(msg) {
        draw2c(msg.data);
        if (off==0) {
            initPager(msg.total)
        }
    }
    phonelist(drawph0,type,brand,q,off)
}
function draw2a(label){
    label.forEach((item, i) => {
        $('#labellist').append('<div class="chooseoptiontext"  id="label'+i+'" onclick="labelclick(this)" >'+item+'</div>');
        labelclickitem = $('#label0');
        $(labelclickitem).attr('class','chooseoptiontext2');
    });
}
function draw2b(model){
    model.forEach((item, i) => {
        $('#modellist').append('<div class="chooseoptiontext"  id="model'+i+'" onclick="modelclick(this)" >'+item+'</div>');
        modelclickitem = $('#model0');
        $(modelclickitem).attr('class','chooseoptiontext2');
    });
}
function draw2c(phoneListData){
    $('.chooseresultshow').html('')
    phoneListData.forEach((item, i) => {
        $('.chooseresultshow').append('<div class="phoneinfo" onclick="onclickphone('+ item.id +')"><div class="mainphone"><div class="mainphonetitle">' + item.model + '</div><img class="mainphoneimg" src="' + item.photo + '" /><div class="mainphoneprice">回收價<span class="mainprice">' + item.price + '</span></div>  <div class="mainrecyclecount">已被詢價<span class="maincount">' + item.count + '</span>次</div></div></div>');
        $('.phoneinfo').click(function() {
            window.location.href = "phoneinfo.html";
        })
    });
}

function gogopage(p){
    // console.log('gogopage:',p);
    var off=(p-1)*16;
    draw2d(off)
}
function initPager(total){
    // console.log('total num recs:',total);
    // if (total<17){
    //     $('#pager').hide()
    // } else {
    //     $('#pager').show()
    // }
    $('#pager').show()
    total=total==0?1:total
    $("#pager").zPager({
        current:1,
        totalData:total,
        pageData:16,
        pageStep:6,
        btnShow:true,
        btnBool:true,
        ajaxSetData: false,
        callback:gogopage,
    });
}

function labelclick(value) {
    $(labelclickitem).attr('class','chooseoptiontext');
    $(value).attr('class','chooseoptiontext2');
    labelclickitem = value;
    // console.log(labelclickitem.id + modelclickitem.id);
    setFilter()
}

function modelclick(value) {
    $(modelclickitem).attr('class','chooseoptiontext');
    $(value).attr('class','chooseoptiontext2');
    modelclickitem = value;
    // console.log(labelclickitem.id + modelclickitem.id);
    setFilter()
}

function setFilter() {
    var text=getSearchText();
    setCache('modelFilter',text)
    var brandFilter = $('.chooseoptiontext2')[0].innerText
    setCache('brandFilter',brandFilter)
    var typeFilter = $('.chooseoptiontext2')[1].innerText
    setCache('typeFilter',typeFilter)
    draw2d(0)
}
function gosearch3(){
    var text=getCache('modelFilter');
    $('#usertext').text(text)
    draw2d(0)
}
