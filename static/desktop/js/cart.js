 $(document).on('click','.add_to_cart',function(e)
      {
      console.log(e);






product_id = $(this).attr('data-id')
                  try {
                      qty = $('#addqty')[0].value
                    }
                    catch(err) {
                      qty = 1
                    }

                  console.log("qty");
                  console.log(qty);
                  data = {
                      product_id: product_id,
                      product_quantity: qty,
                      csrfmiddlewaretoken: csrf,
                  }

                  $.ajax({
                      type: 'POST',
                      url: '/order/addtocart/',
                      data: data,
                      success: function(data){
                      $("#checkout_button").css("display", "flex");
                        $("#indicator__counter").trigger('reset');
                        $("#indicator__counter").empty();
                           $("#indicator__counter").prepend(`${data["qty"]||"0"}`);

                           $("#indicator__counter_mobile").trigger('reset');
                        $("#indicator__counter_mobile").empty();
                           $("#indicator__counter_mobile").prepend(`${data["qty"]||"0"}`);

                           $("#indicator__counter_mobile2").trigger('reset');
                        $("#indicator__counter_mobile2").empty();
                           $("#indicator__counter_mobile2").prepend(`${data["qty"]||"0"}`);



                        $("#cart_summary").trigger('reset');
                        $("#cart_summary").empty();
                           $("#cart_summary").prepend(`₼ ${data["summary"]||""}`);

                           $("#cart_summary_inside1").trigger('reset');
                        $("#cart_summary_inside1").empty();
                           $("#cart_summary_inside1").prepend(`₼ ${data["summary"]||"0"}`);

                           $("#cart_summary_inside2").trigger('reset');
                        $("#cart_summary_inside2").empty();
                           $("#cart_summary_inside2").prepend(`₼ ${data["summary"]||"0"}`);

                        $("#cart_inside").trigger('reset');
                        $("#cart_inside").empty();
                      for (let i = 0; i < data["products"].length; i++) {
                        $("#cart_inside").prepend(`<li class="dropcart__item">
                                 <div class="dropcart__item-image image image--type--product"><a class="image__body" href="#"><img style="    width: 100%;" class="image__tag" src="${data["products"][i]["image"]||""}" alt=""></a></div>
                                 <div class="dropcart__item-info" style="width: 56%;">
                                    <div class="dropcart__item-name"><a href="#">${data["products"][i]["name"]||""}</a></div>
                                    <ul class="dropcart__item-features">
                                       <li>${data["products"][i]["cat"]||""}</li>

                                    </ul>
                                    <div class="dropcart__item-meta">
                                       <div class="dropcart__item-quantity">${data["products"][i]["qty"]||""}</div>
                                       <div class="dropcart__item-price">₼ ${data["products"][i]["price"]||""}</div>
                                    </div>
                                 </div>
                                 <button type="button" id="${data["products"][i]["item_id"]||""}"   onclick="onCatClick(${data["products"][i]["item_id"]||""})" class="remove dropcart__item-remove" style=" margin-top: 21px; ">
                                    <svg width="10" height="10">
                                       <path d="M8.8,8.8L8.8,8.8c-0.4,0.4-1,0.4-1.4,0L5,6.4L2.6,8.8c-0.4,0.4-1,0.4-1.4,0l0,0c-0.4-0.4-0.4-1,0-1.4L3.6,5L1.2,2.6
                                          c-0.4-0.4-0.4-1,0-1.4l0,0c0.4-0.4,1-0.4,1.4,0L5,3.6l2.4-2.4c0.4-0.4,1-0.4,1.4,0l0,0c0.4,0.4,0.4,1,0,1.4L6.4,5l2.4,2.4
                                          C9.2,7.8,9.2,8.4,8.8,8.8z"></path>
                                    </svg>
                                 </button>
                              </li>
                              <li class="dropcart__divider" role="presentation"></li>`)
                     }


        var menuu = $(".js-menu__open").attr('data-menu');

        $(menuu).toggleClass('js-menu__expanded');
        $(menuu).parent().toggleClass('js-menu__expanded');

 document.body.style.overflow = 'hidden';


console.log("hehe");



                      }
                  })
                  })


