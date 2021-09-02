var timer = null;
var timerInterval = null;

$( document ).ready(function() {
    function createGame(mx, my) {
        let h = 100 / my;
        let w = 100 / mx;

        for (let y = 0; y < my; y++) {
            for (let x = 0; x < mx; x++) {

                let e = $("<div class='cell closed' data-x='" + x + "' data-y='" + y + "'></div>")

                e.css('height', h + '%');
                e.css('width', w + '%');

                e.contextmenu(function() {
                    if ($(this).hasClass("closed")) {
                        let flag = $("<p>!</p>");

                        $(this).append(flag);

                        $(this).removeClass("closed");
                        $(this).addClass("flag");
                        updateMineCounter(-1);
                    } else {
                        $(this).find("p").remove();
                        $(this).removeClass("flag");
                        $(this).addClass("closed");
                        updateMineCounter(1);
                    }

                    if (timerInterval === null) {
                        timerInterval = setInterval(updateTimer, 1000);
                    }

                    return false;
                });

                $('.field').append(e)
            }
        }
    }

    function getCell(x, y) {
        return $(".cell[data-x='" + x + "'][data-y='" + y + "']")
    }

    function openCells(to_open) {
        to_open.forEach((data, i) => {
            let cell = getCell(data[0], data[1]);

            cell.removeClass("closed");
            cell.addClass("open");

            if (data[2] !== 0) {
                cell.text(data[2]);
            }
        });
    }

    function detonate(mines) {
        mines.forEach((mine, i) => {
            let cell = getCell(mine[0], mine[1]);

            cell.removeClass("closed");
            cell.addClass("bomb");
        });

        $(".give-up a").text("You Died !!!");
        $(".give-up a").removeClass("btn-info");
        $(".give-up a").addClass("btn-danger");
        $(".game").addClass("disable-click")
    }

    function updateMineCounter(num) {
        if (num === 1 || num === -1) {
            let newValue = $(".mines-counter").data("mines") + num;
            $(".mines-counter").data("mines", newValue);

            if (newValue >= 0) {
                $(".mines-counter span").text(("000" + newValue).substr(-3));
            } else {
                let vstr = ("000" + (0 - newValue)).substr(-3)
                $(".mines-counter span").text("-" + vstr);
            }
        } else {
            $(".mines-counter").data("mines", num);
            $(".mines-counter span").text(("000" + num).substr(-3));
        }
    }

    function updateTimer() {
        timer = timer + 1;
        $(".seconds-counter span").text(("000" + timer).substr(-3));
    }

    function deleteGame() {
        let csrftoken = $("#csrf").data("token");

        $.ajax({
            type: "DELETE",
            url: $(".levels").data("url") + "/" + $(".game").data("id"),
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    }

    $(".levels div p a").on("click", function() {
        let x = $(this).data("x");
        let y = $(this).data("y");
        let mines = $(this).data("mines");
        let fsize = parseFloat($(this).data("fsize"));
        let csrftoken = $("#csrf").data("token");

        $.ajax({
            type: "POST",
            url: $(".levels").data("url"),
            data: JSON.stringify({
                x: x,
                y: y,
                mines: mines
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data) {
                $(".cell").remove();
                createGame(x,y);
                updateMineCounter(mines);
                $(".give-up a").text("Give up")
                $(".give-up a").removeClass("btn-danger");
                $(".give-up a").addClass("btn-info");
                $(".game").removeClass("disable-click")
                $(".levels").addClass("hidden");
                $(".title").addClass("hidden");
                $(".game").removeClass("hidden");
                $(".game").data("id", data.game_id);
                $(".field").fitText(fsize);
                $(".seconds-counter span").text("000");
                timer = 0;
            }
        });
    });

    $(".give-up a").on("click", function() {
        $(".levels").removeClass("hidden");
        $(".title").removeClass("hidden");
        $(".game").addClass("hidden");
        clearInterval(timerInterval);
        timerInterval = null;
        deleteGame();
    });

    $(document).on("click", ".closed", function(e) {
        if ($(".game").hasClass("disable-click")) {
            return;
        }

        if (timerInterval === null) {
            timerInterval = setInterval(updateTimer, 1000);
        }

        $.ajax({
            type: "GET",
            url: $(".levels").data("url") + "/" + $(this).data("x") + "/" + $(this).data("y") + "/" + $(".game").data("id"),
            success: function(data) {
                if (data.result === "game-over") {
                    detonate(data.mines);
                    clearInterval(timerInterval);
                    timerInterval = null;
                } else {
                    openCells(data.opened);

                    if (data.result === "won") {
                        $(".closed").each(function() {
                            let flag = $("<p>!</p>");

                            $(this).append(flag);
                        });

                        $(".give-up a").text("You Win !!!");
                        $(".give-up a").removeClass("btn-info");
                        $(".give-up a").addClass("btn-success");
                        $(".game").addClass("disable-click")
                        clearInterval(timerInterval);
                        timerInterval = null;
                        updateMineCounter(0);
                    }
                }
            }
        });
    });

    $(window).bind('beforeunload',function(){
        deleteGame()
    });
});
