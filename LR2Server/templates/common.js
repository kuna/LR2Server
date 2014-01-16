
$(document).ready(function() {
	$(".bmsfile").hide();

	i = 1;
	while ($("#a" + i).length) {
		$("#a" + i).click(function() {
			ni = $(this).attr("id").substring(1);
			$("#u" + ni).toggle();
			return false; // prevent scrolling to top
		});
		i++;
	}

	// add exlevel information
	$(".bmsfile_li").each(function(e) {
		if (parseInt($(this).data('exlevel')) > 0) {
			$(this).find(".desc").append(" (★" + $(this).data('exlevel') + ")");
		}
	});

	// add checkbox handler
	$("#searchOption input:checkbox").click(function() {
		showItem();
	});

	// add combobox handler
	$("#grade").change(function() {
		showGrade($("#grade").val());
	});

	// score
	$(".score").each(function () {
		var rank = $(this).find(".rank");
		var clear = $(this).find(".clear");

		var ranknum = parseInt(rank.html());
		var clearnum = parseInt(clear.html());
		if (ranknum >= 8) {
			rank.html("<img src='" + relpath + "img/rA.png'>" +
				"<img src='" + relpath + "img/rA.png'>" +
				"<img src='" + relpath + "img/rA.png'>"
				);
		} else if (ranknum >= 7) {
			rank.html("<img src='" + relpath + "img/rA.png'>" +
				"<img src='" + relpath + "img/rA.png'>"
				);
		} else if (ranknum >= 6) {
			rank.html("<img src='" + relpath + "img/rA.png'>"
				);
		} else if (ranknum >= 5) {
			rank.html("<img src='" + relpath + "img/rB.png'>");
		} else if (ranknum >= 4) {
			rank.html("<img src='" + relpath + "img/rC.png'>");
		} else if (ranknum >= 3) {
			rank.html("<img src='" + relpath + "img/rD.png'>");
		} else if (ranknum >= 2) {
			rank.html("<img src='" + relpath + "img/rE.png'>");
		} else {
			rank.html("<img src='" + relpath + "img/rF.png'>");
		}

		if (clearnum >= 5) {
			clear.html("<span class='c_fc'>FULL COMBO</span>");
		} else if (clearnum >= 4) {
			clear.html("<span class='c_hd'>HARD CLEAR</span>");
		} else if (clearnum >= 3) {
			clear.html("<span class='c_normal'>GROOVE CLEAR</span>");
		} else if (clearnum >= 2) {
			clear.html("<span class='c_easy'>EASY CLEAR</span>");
		} else {
			clear.html("<span class='c_fail'>FAILED</span>");
		}
	});
});

function showGrade(v) {
	if (v == "none") {
		showAll();
	} else {
		showOnlyHash(v);
	}
}

function showOnlyHash(hashstr) {
	var l = hashstr.length;
	var hl = new Array();
	for (nl=0; nl<l; nl+=32) {
		hl.push(hashstr.substring(nl, nl+32))
	}

	// search items
	$("#songitem .songele").each(function(e) {
		var isFound = false;
		$.each($(this).find(".bmsfile_li"), function (e) {
			for (i=0; i<hl.length; i++) {
				if ($(this).data('hash') == hl[i]) {
					isFound = true;
					break;
				}
			}
		});

		if (!isFound) {
			$(this).hide();
		} else {
			$(this).show();
		}
	});
}

function showItem() {
	// get condition
	keyarr = new Array();
	lvl_normal = new Array();
	lvl_insane = new Array();

	mode = 0;
	i = 0;
	filterKey = false;
	filterNormal = false;
	filterInsane = false;
	filterText = false;
	searchText = $("#searchText").val();
	if (searchText.length > 0) {
		filterText = true;
	}
	isShowAll = true;
	$("#searchOption input:checkbox").each(function(e) {
		if (mode == 0) {
			// parsing key
			keyarr[i] = this.checked;
			if (this.checked) {
				filterKey = true;
			}

			i += 1;
			if (i >= 5) {
				i = 0;
				mode = 1;
			}
		} else if (mode == 1) {
			// parsing lvl
			lvl_normal[i] = this.checked;
			if (this.checked) {
				filterNormal = true;
			}

			i += 1;
			if (i >= 13) {
				i = 0;
				mode = 2;
			}
		} else if (mode == 2) {
			// parsing insane lvl
			lvl_insane[i] = this.checked;
			if (this.checked) {
				filterInsane = true;
			}

			i += 1;
			if (i >= 26) {
				i = 0;
				mode = 3;	// do nothing
			}
		}

		if (this.checked) {
			isShowAll = false;
		}
	});

	if (isShowAll && !filterText) {
		showAll();
	} else {
		$("#songitem .songele").each(function(e) {
			var isFound = false;
			var datapath = $(this).data('path');

			$.each($(this).find(".bmsfile_li"), function (e) {
				var cond = true;

				if (filterKey && cond) {
					var keycnt = parseInt($(this).data('key'));
					var keyind = -1;
					if (keycnt == 5) {
						keyind = 0;
					} else if (keycnt == 7) {
						keyind = 1;
					} else if (keycnt == 9) {
						keyind = 2;
					} else if (keycnt == 10) {
						keyind = 3;
					} else if (keycnt == 14) {
						keyind = 4;
					}

					if (!(keyind>=0 && keyarr[keyind])) {
						cond = false;
					}
				}

				if (filterNormal && cond) {
					var lvl = parseInt($(this).data('level'))-1;
					if (!(lvl>=0 && lvl_normal[lvl])) {
						cond = false;
					}
				}

				if (filterInsane && cond) {
					var lvlinsane = parseInt($(this).data('exlevel'))-1;
					if (!(lvlinsane>=0 && lvl_insane[lvlinsane])) {
						cond = false;
					}
				}

				if (filterText && cond) {
					if ($(this).data('title').toString().search(new RegExp(searchText,'i')) < 0 && datapath.search(new RegExp(searchText, 'i')) < 0) {
						cond = false;
					}
				}

				if (cond) {
					isFound = true;
				}
			});

			if (!isFound) {
				$(this).hide();
			} else {
				$(this).show();
			}
		});
	}
}

function showAll() {
	$("#songitem .songele").show();
}

function sortName() {
	$("#songitem .songele").sort(function(a,b) {
	     return a.dataset.sid > b.dataset.sid ? 1 : -1;
	}).appendTo('#songitem');
}

function sortDate() {
	$("#songitem .songele").sort(function(a,b) {
	     return parseInt(a.dataset.date) - parseInt(b.dataset.date);
	}).appendTo('#songitem');
}