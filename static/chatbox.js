(function ($) {

    var pre_me_say = "";

    $(document).ready(function (evt) {

        // 初始化时清除输入框的记忆功能
        $(".panel-chatbot input[name=utterance]").val("");


        // bind evts
        $("a[name=send-btn]").bind("click", function (evt) {
            send_text();
        });

        $(".panel-chatbot input[name=utterance]").bind("keypress", function (evt) {

           if(evt.keyCode == 13){
               send_text();
           }

        });

        // $(".panel-chatbot input[name=utterance]").bind("keyup", function (evt) {
        //
        //     var val = $(this).val();
        //     if(val.length >= 2){
        //         get_tips(val);
        //     }
        //     else{
        //         $("ul.auto_tips").hide();
        //     }
        //
        // });
        //
        // $("ul.auto_tips").on("click", "a", function (evt) {
        //     var text = $(this).text();
        //     $(".panel-chatbot input[name=utterance]").val(text);
        //     send_text();
        //     $("ul.auto_tips").hide();
        // });
        //
        // $(".panel-chatbot .body").on("click", "a.question", function (evt) {
        //     var text = $(this).text();
        //     var theme = $(this).parent("p").data("theme");
        //     $(".panel-chatbot input[name=utterance]").val(text);
        //     send_text(theme);
        //
        // });


        $(".qa_cls>.list-group a").on("click", function (evt) {
           $(this).siblings().removeClass("active");
           $(this).addClass("active");

        });

        $(document).bind("add_say_text", function (evt, who, say_text) {

            if(who == "Me"){
                pre_me_say = say_text;
                return;
            }

            setTimeout(function () {
                $(".panel-chatbot>.body div.say-item.robot:last>p:last").hide().slideDown(function () {
                    $(".panel-chatbot>.body").scrollTop(1000000);
                });
            }, 200);

        });


        $("body").on("click", function (evt) {
           if(!$(evt.target).is(".auto_tips li a")){
               $(".auto_tips").hide();
           }
        });

        $(document).on("not_answers", function (evt) {
            get_questions();
        })


        $("#myModalA button.btn-submit").on("click", function (evt) {
            create_qa();
        });

        //end bind evts

    });

    var render_template = function (name, data) {
        var _html = $("#templates>script[name=" + name + "]").text();
        var template = _.template(_html);
        return template(data);
    };


    var pop_alert = function(content, atype){
        if(! atype){
            atype = "success";
        }
        if(!pop_alert._num){pop_alert._num = 1;}
        pop_alert._num += 1;

        var _num = pop_alert._num;
        var html = render_template("alert", {content:content, atype:atype, num:_num});
        $("#op_tip_div").append(html);

        setTimeout(function () {
            $("#op_tip_div .alert_num_" + _num).alert("close");
        }, 1000*4)

    };


    var get_theme=function(){
      var theme = $(".qa_cls>.list-group a.active").text();
      return theme;
    };

    var get_questions =function(){
        var theme = get_theme();

        $.ajax({
            type: "GET",
            url: "/question",
            dataType: "json",
            data: {theme:theme},
            success: function (result) {
                if(! result || result.length == 0){
                    return;
                }

                var html = render_template("say_guess_item", {result:result, theme:theme});
                $(".panel-chatbot>.body").append(html);
                $(".panel-chatbot>.body").scrollTop(1000000);

            }
        });


    };

    var get_tips = function(text){
        var theme = get_theme();
        $.ajax({
            type: "GET",
            url: "/api/web",
            dataType: "json",
            data: {text: text, theme:theme},
            success: function (result) {
                var html = render_template("tip_item", {result:result});
                if(result.length > 0){
                    $("ul.auto_tips").show();
                    $("ul.auto_tips").html("").append(html);
                }
                else{
                    $("ul.auto_tips").hide();
                }
            }
        });

    };

    var send_text = function (theme) {

        /**
        var ctx_id = $.trim($(".panel-settings input[name=ctx_id]").val());
        if(!/^\w{6,12}$/.test(ctx_id)){
            alert("未正确设置会话ID");
            return;
        }
        */
        var utterance_input = $(".panel-chatbot input[name=utterance]");
        var utterance = $.trim(utterance_input.val());
        if(utterance == ""){return}

        utterance_input.val("");

        add_say_text("Me", utterance);


        var theme = theme || get_theme();

        $.ajax({
            type: "GET",
            url: "/api/web",
            dataType: "json",
            data: {text: utterance, theme:theme},
            success: function (result) {
                if(! result || result.length == 0){
                    $(document).trigger("not_answers");
                    return;
                }
                add_say_text("Robot", result[0]);
                $(".panel-chatbot>.body").scrollTop(1000000);
            }
        });


    };

    var create_qa = function () {

        var theme = $.trim($("#myModalA select[name=theme]").val());
        var question = $.trim($("#myModalA input[name=question]").val());
        var answer = $.trim($("#myModalA textarea[name=answer]").val());
        if(theme == "" || question == "" || answer == ""){
            pop_alert("提交失败", "danger");
            return;
        }


        $.ajax({
            type: "GET",
            url: "/create_qa",
            dataType: "json",
            data: {theme: theme, question:question, answer:answer},
            success: function (result) {
                $("#myModalA form").get(0).reset();
                pop_alert("操作完成");
            }
        });

    };

    var add_say_text = function (who, text) {
        var html = render_template("say_item", {who:who, text: text});
        $(".panel-chatbot>.body").append(html);

        $(document).trigger("add_say_text", [who, text]);


    };







})(jQuery);