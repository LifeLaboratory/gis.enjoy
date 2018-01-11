$prevButton = $("#prev-step");
$nextButton = $("#next-step");

function countSteps() {
    var is = true;
    var i = 0;
    while (is) {
        if (!document.getElementById("step" + i)) {
            is = false;
            continue;
        }
        i++;
    }
    return i;
}

function switchStep(direction) {
    alert("switchStep");


    switch(direction) {
        case 'next':
            if ($step === 0) {
                takeAddress();
            }

            if ($step != $lastStep) {
                console.log("switch next");
                console.log($("step" + $step));
                $("#step" + $step).addClass("disabled-block");
                $step++;
                $("#step" + $step).removeClass("disabled-block");
            }


            break;
        case 'prev':
            if($step){
                $("#step" + $step).addClass("disabled-block");
                $step--;
                $("#step" + $step).removeClass("disabled-block");
            }
            break;
        default:
            break;
    }

    debugger;
    console.log($step === $lastStep);

    if ($step === $lastStep) {
        $("#next").html('<button id="show-routes" class="select-options__next-button">Показать маршруты</button>');
        
        $("#show-routes").click(function () {
            sendResult();
        });
    } else {
        $("#next").html('<button id="next-step" class="select-options__next-button">Далее</button>');
        console.log("elseee");
        $("#next-step").click(function () {
            console.log("next button click");
            switchStep("next");
        });
    }

    console.log("Step = " + $step);
}

function zeroStep() {
    $step = 0;
    console.log("step=" + $step);
    $("#next").html('<button id="show-routes" class="select-options__next-button">Далее</button>');
}

$nextButton.click(function () {
    console.log("next button click");
    switchStep("next");
});

$prevButton.click(function () {
    console.log("prev button click");
    switchStep("prev");
});

$step = 0;
$lastStep = countSteps() - 1;