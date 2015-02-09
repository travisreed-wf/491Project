<script type="text/javascript">

  function createElement(elementWell, elementToCreate){
      $('#elementWell').css("height","100px");
      $('#elementWell').html("<br><br>Add more elements here.");
      elementWell.before("<div class='elementTarget'></div>");
      var target = elementWell.parent().find(".elementTarget").first();
      target.load(elementToCreate.data('filepath'));
      target.hide().fadeIn(700);
      target.removeClass('elementTarget');
      return target;
  }
  function makeDroppable(element){
    element.droppable({
      drop: function(event, ui){
        var elementWell = $(this);
        var element = ui.draggable;
        var newElement = createElement(elementWell, element);
        makeDroppable(newElement);     
      }
    })
  }
  function getVideoURL(original){
    // will likely need to add more url handlers later, 
    // for now we support youtube urls
    if(original.indexOf("<iframe") >= 0){
      var src = original.substring(original.indexOf('src="')+5);
      src = src.substring(0,src.indexOf('"'));
      return src;
    } else if(original.indexOf("watch?v=") >= 0){
      return original.replace("watch?v=","embed/")
    } else {
      return original;
    }
  }

  function updateVideoSRC(changeEvent){
    var src = getVideoURL($(changeEvent).val());
    $(changeEvent).parent().find('.wp-video-panel').attr("src", src)
  }

  function clickVideo(clkevent){
    var src = $(clkevent).parent().find('.wp-video-panel').attr('src');
    $(clkevent).parent().find('iframe').attr('src', src);
    $(clkevent).parent().find('.modal').modal('toggle');
    $('.modal').on('hidden.bs.modal', function () {
      $('iframe').attr('src', $('iframe').attr('src'));
    });
  }
  function clickImage(clkevent){
    console.log($(clkevent).parent().find('img').attr('src'));
    var src = $(clkevent).parent().find('img').attr('src');
    $(clkevent).parent().find('iframe').attr('src', src);
    $(clkevent).parent().find('.modal').modal('toggle');
    $('.modal').on('hidden.bs.modal', function () {
      $('iframe').attr('src', $('iframe').attr('src'));
    });
  }
  function clickFile(clkevent){
    var src = $(clkevent).parent().find('.wp-file-title-label').attr('src');
    console.log(src);
    $(clkevent).parent().find('iframe').attr('src', src);
    $(clkevent).parent().find('.modal').modal('toggle');
    $('.modal').on('hidden.bs.modal', function () {
      $('iframe').attr('src', $('iframe').attr('src'));
    });
  }

  function addVideo(ctx){
    $(ctx).closest('.panel-body').find('.supplementary-target').append($('#wp-video-template').html());
  };
  function addAudio(ctx){
    $(ctx).closest('.panel-body').find('.supplementary-target').append($('#wp-audio-template').html());
  };
  function addText(ctx){
    $(ctx).closest('.panel-body').find('.supplementary-target').append($('#wp-text-template').html());
  };
  //Also used for other file upload
  function addImage(ctx){
    $(ctx).closest('.panel-body').find('.supplementary-target').append($('#wp-image-template').html());
  };
  function addOtherFile(ctx){
    $(ctx).closest('.panel-body').find('.supplementary-target').append($('#wp-file-template').html());
  };

  function uploadImageFile(f) {
      var form_data = new FormData(f);
      $.ajax({
          type: 'POST',
          url: '/upload',
          data: form_data,
          contentType: false,
          cache: false,
          processData: false,
          async: false,
          success: function(data) {
            var src = $(f).find('input').val();
            var src = src.split("\\")[2]
            src = "/static/uploads/" + src;
            $(f).closest('div.wp-image').find('img').first().attr("src", src);
          },
      });
  };
  function uploadFile(f) {
      var form_data = new FormData(f);
      $.ajax({
          type: 'POST',
          url: '/upload',
          data: form_data,
          contentType: false,
          cache: false,
          processData: false,
          async: false,
          success: function(data) {
            var src = $(f).find('input.wp-file-src').val();
            var src = src.split("\\")[2];
            src = "/static/uploads/" + src;
            $(f).parent().parent().find('h3').first().attr("src", src);
          },
      });
  };

  function changeTitle(element){
    $(element).closest('div.wp-file').find('h3').text($(element).val());
  }


  function textChange(element){
    var id_str = "#p_" + $(element).attr('id');
    $(element).parent().find(id_str).text($(element).val());
  }
  function textChangeBySibling(element){
    var id_str = "#p_" + $(element).attr('id');
    $(element).next('p').text($(element).val());
  }

  function deleteAllQuestions(){
    $('#questionList').find('.question-parent').each(function(){
      var toDel = $(this);
      toDel.fadeOut(200, function(){toDel.remove()});
    });
    $('#elementWell').css("height","300px");
    $('#elementWell').html("<br><br>To begin, drag elements onto the screen.");
  }
</script>
