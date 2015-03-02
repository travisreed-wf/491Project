<script type="text/javascript">
  
  var supplementaryInformationTimes = {}; 
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

  function modalTiming(event){
    var endDate = new Date();
    var endTime = endDate.getTime();
    var duration = endTime - event.data.startTime;
    $('.modal').data("supplementaryDuration",duration/1000);
    alert($('.modal').data("supplementaryDuration"));
    alert(event.data.modalID);
    if(supplementaryInformationTimes[event.data.modalID]){
          supplementaryInformationTimes[event.data.modalID] = supplementaryInformationTimes[event.data.modalID] + duration/1000;
    }else{
          supplementaryInformationTimes[event.data.modalID] = duration/1000;
    }
    alert(supplementaryInformationTimes[event.data.modalID] + "  :alsdjfl;aksdf;lakd");
    $('.modal').off('hide.bs.modal');       
    
  }

  function clickVideo(clkevent){
    var src = $(clkevent).parent().find('.wp-video-panel').attr('src');
    $(clkevent).parent().find('iframe').attr('src', src);
    var modal = $(clkevent).parent().find('.modal');
    modal.modal('toggle');
    var startDate = new Date();
    $('.modal').data("supplementaryDuration",startTime);
    $('.modal').on('hidden.bs.modal', function () {
      $('iframe').attr('src', $('iframe').attr('src'));
    }); 
    var modalID = $(modal).attr('id');
    var startTime = startDate.getTime();
    $('.modal').on('hide.bs.modal', {startTime: startTime, modalID: modalID}, modalTiming);
  }
  function clickImage(clkevent){
    console.log($(clkevent).parent().find('img').attr('src'));
    var src = $(clkevent).parent().find('img').attr('src');
    $(clkevent).parent().find('iframe').attr('src', src);
    var modal = $(clkevent).parent().find('.modal');
    modal.modal('toggle');    
    var startDate = new Date();
    $('.modal').on('hidden.bs.modal', function () {
      $('iframe').attr('src', $('iframe').attr('src'));
    });
    var modalID = $(modal).attr('id');
    var startTime = startDate.getTime();
    $('.modal').on('hide.bs.modal', {startTime: startTime, modalID: modalID}, modalTiming);

  }
  function clickFile(clkevent){
    var src = $(clkevent).parent().find('.wp-file-title-label').attr('src');
    console.log(src);
    $(clkevent).parent().find('iframe').attr('src', src);
    var modal = $(clkevent).parent().find('.modal');
    modal.modal('toggle');    
    var startDate = new Date();    
    $('.modal').on('hidden.bs.modal', function () {
      $('iframe').attr('src', $('iframe').attr('src'));
    });
    var modalID = $(modal).attr('id');
    var startTime = startDate.getTime();
    $('.modal').on('hide.bs.modal', {startTime: startTime, modalID: modalID}, modalTiming);

  }

  function addSuppElement(ctx, appendID){
    var toAppend = $(ctx).closest('.panel-body').find('.supplementary-target');
    var html = $(appendID).html();
    html = html.replace("nextID", nextSupplementaryID);
    nextSupplementaryID = "supplementary" + (parseInt(nextSupplementaryID.split("supplementary")[1]) + 1);
    toAppend.append(html);
  }
  function addVideo(ctx){
    addSuppElement(ctx, '#wp-video-template')
  };
  function addAudio(ctx){
    addSuppElement(ctx, '#wp-audio-template')
  };
  function addText(ctx){
    addSuppElement(ctx, '#wp-text-template')
  };
  //Also used for other file upload
  function addImage(ctx){
    addSuppElement(ctx, '#wp-image-template')
  };
  function addOtherFile(ctx){
    addSuppElement(ctx, '#wp-file-template')
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

  function textChange1Parent(element){
    var id_str = "#p_" + $(element).attr('id');
    $(element).parent().find(id_str).text($(element).val());
  }
  function textChange(element){
    var id_str = "#p_" + $(element).attr('id');
    $(element).parent().parent().find(id_str).text($(element).val());
  }
  function textChangeBySibling(element){
    var id_str = "#p_" + $(element).attr('id');
    $(element).next('p').text($(element).val());
  }

  function getCoursesTeaching(){
    $.ajax({
      url         :'{{ url_for("courses_teaching")}}',
      type        :"GET",
      success     :function(result) {
          var coursesList = $.parseJSON(result);
          
          var strCoursesList="";
          for(var i=0; i < coursesList.length;i++){
              url = "{{url_for('view_course', courseID='')}}";
              url += coursesList[i].id + 1000;
              strCoursesList+="<li class='submit-task' id='" + coursesList[i].id + "' onclick='submitClicked(this)''><a target='" + url + "'>";
              strCoursesList+=coursesList[i].name;
              strCoursesList+="</a></li>";
          }
          if(coursesList.length == 0){
              strCoursesList+="<a href='#' class='list-group-item'>No Courses</a>";
          }
          $('#taskbuilder_viewable_courses').html(strCoursesList);
      }
    });
  }

  function deleteAllQuestions(){
    $('#elementWell').css("height","300px");
    $('#elementWell').html("<br><br>To begin, drag elements onto the screen.");
    $('#questionList').find('.question-parent').each(function(){
      var toDel = $(this);
      toDel.fadeOut(200, function(){toDel.remove()});
    });
  }

  function submitClicked(element) {
      console.log("click hit");
      $('.EDIT_ONLY').remove();
      $('.PREVIEW_ONLY').remove();
      var questions = [];
      $('.automatic-grading').each(function(){
          var question = $(this);
          var data = {};
          data['options'] = [];
          data['questionID'] = question.attr('id');
          question.find(':radio:visible').each(function(){
            data['options'].push($(this).attr('id'));
          });
          data['correctOption'] = question.find(':radio:checked').attr('id');
          questions.push(data);
      })
      var data = {};
      data['html'] = $('#questionList').html();
      data['questions'] = questions;
      console.log($(element).attr('id'));
      data['course_id'] = $(element).attr('id');
      data['supplementary'] = supplementaryInformationTimes;
      $.ajax({
          url: '{{ url_for("taskBuilder") }}',
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(data),
          success: function(data){
            window.location.href='{{url_for("home")}}';
          },
          error: function(data){
              console.log(data);
          }
      });
  }

</script>
