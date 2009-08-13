// Inserts shortcut buttons after all of the following:
//     <input type="text" class="vDateField">

var DateTimeShortcuts = {
    calendars: [],
    calendarInputs: [],
    calendarDivName1: 'calendarbox', // name of calendar <div> that gets toggled
    calendarDivName2: 'calendarin',  // name of <div> that contains calendar
    calendarLinkName: 'calendarlink',// name of the link that is used to toggle
    admin_media_prefix: '',
    init: function() {
        // Deduce admin_media_prefix by looking at the <script>s in the
        // current document and finding the URL of *this* module.
        var scripts = document.getElementsByTagName('script');
        for (var i=0; i<scripts.length; i++) {
            if (scripts[i].src.match(/calendar/)) {
                var idx = scripts[i].src.indexOf('js/calendar');
                DateTimeShortcuts.admin_media_prefix = scripts[i].src.substring(0, idx);
                break;
            }
        }

        var inputs = document.getElementsByTagName('input');
        for (i=0; i<inputs.length; i++) {
            var inp = inputs[i];
            if (inp.getAttribute('type') == 'text' && inp.className.match(/vDateField/)) {
                DateTimeShortcuts.addCalendar(inp);
            }
        }
    },

    // Add calendar widget to a given field.
    addCalendar: function(inp) {
        var num = DateTimeShortcuts.calendars.length;

        DateTimeShortcuts.calendarInputs[num] = inp;

        // Shortcut links (calendar icon and "Today" link)
        var shortcuts_span = document.createElement('span');
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
/*        var today_link = document.createElement('a');
        today_link.setAttribute('href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', 0);');
        today_link.appendChild(document.createTextNode(gettext('Today')));*/
        var cal_link = document.createElement('a');
        cal_link.setAttribute('href', 'javascript:DateTimeShortcuts.openCalendar(' + num + ');');
        cal_link.id = DateTimeShortcuts.calendarLinkName + num;
        quickElement('img', cal_link, '', 'src', DateTimeShortcuts.admin_media_prefix + 'img/admin/icon_calendar.gif', 'alt', gettext('Calendar'));
        shortcuts_span.appendChild(document.createTextNode('\240'));
        //shortcuts_span.appendChild(today_link);
        shortcuts_span.appendChild(cal_link);

        // Create calendarbox div.
        //
        // Markup looks like:
        //
        // <div id="calendarbox3" class="calendarbox module">
        //     <h2>
        //           <a href="#" class="link-previous">&lsaquo;</a>
        //           <a href="#" class="link-next">&rsaquo;</a> February 2003
        //     </h2>
        //     <div class="calendar" id="calendarin3">
        //         <!-- (cal) -->
        //     </div>
        //     <div class="calendar-shortcuts">
        //          <a href="#">Yesterday</a> | <a href="#">Today</a> | <a href="#">Tomorrow</a>
        //     </div>
        //     <p class="calendar-cancel"><a href="#">Cancel</a></p>
        // </div>
        var cal_box = document.createElement('div');
        cal_box.style.display = 'none';
        cal_box.style.position = 'absolute';
        cal_box.className = 'calendarbox module';
        cal_box.setAttribute('id', DateTimeShortcuts.calendarDivName1 + num);
        document.body.appendChild(cal_box);
        addEvent(cal_box, 'click', DateTimeShortcuts.cancelEventPropagation);

        // next-prev links
        var cal_nav = quickElement('div', cal_box, '');
	var cal_nav_prev_y = quickElement('a', cal_nav, '<<', 'href', 'javascript:DateTimeShortcuts.drawPrevY('+num+');');
        cal_nav_prev_y.className = 'calendarnav-previous-y';
        var cal_nav_prev = quickElement('a', cal_nav, '<', 'href', 'javascript:DateTimeShortcuts.drawPrev('+num+');');
        cal_nav_prev.className = 'calendarnav-previous';
        var cal_nav_next = quickElement('a', cal_nav, '>', 'href', 'javascript:DateTimeShortcuts.drawNext('+num+');');
        cal_nav_next.className = 'calendarnav-next';
        var cal_nav_next_y = quickElement('a', cal_nav, '>>', 'href', 'javascript:DateTimeShortcuts.drawNextY('+num+');');
        cal_nav_next_y.className = 'calendarnav-next-y';


        // main box
        var cal_main = quickElement('div', cal_box, '', 'id', DateTimeShortcuts.calendarDivName2 + num);
        cal_main.className = 'calendar';
        DateTimeShortcuts.calendars[num] = new Calendar(DateTimeShortcuts.calendarDivName2 + num, DateTimeShortcuts.handleCalendarCallback(num));
        DateTimeShortcuts.calendars[num].drawCurrent();

        // calendar shortcuts
        var shortcuts = quickElement('div', cal_box, '');
        shortcuts.className = 'calendar-shortcuts';
        quickElement('a', shortcuts, gettext('Yesterday'), 'href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', -1);');
        shortcuts.appendChild(document.createTextNode('\240|\240'));
        quickElement('a', shortcuts, gettext('Today'), 'href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', 0);');
        shortcuts.appendChild(document.createTextNode('\240|\240'));
        quickElement('a', shortcuts, gettext('Tomorrow'), 'href', 'javascript:DateTimeShortcuts.handleCalendarQuickLink(' + num + ', +1);');

        // cancel bar
        var cancel_p = quickElement('p', cal_box, '');
        cancel_p.className = 'calendar-cancel';
        quickElement('a', cancel_p, gettext('Cancel'), 'href', 'javascript:DateTimeShortcuts.dismissCalendar(' + num + ');');
    },
    openCalendar: function(num) {
        var cal_box = document.getElementById(DateTimeShortcuts.calendarDivName1+num)
        var cal_link = document.getElementById(DateTimeShortcuts.calendarLinkName+num)
	var inp = DateTimeShortcuts.calendarInputs[num];

	// Determine if the current value in the input has a valid date.
	// If so, draw the calendar with that date's year and month.
	if (inp.value) {
	    var date_parts = inp.value.split('-');
	    var year = date_parts[0];
	    var month = parseFloat(date_parts[1]);
	    if (year.match(/\d\d\d\d/) && month >= 1 && month <= 12) {
		DateTimeShortcuts.calendars[num].drawDate(month, year);
	    }
	}

    
        // Recalculate the clockbox position
        // is it left-to-right or right-to-left layout ?
        if (getStyle(document.body,'direction')!='rtl') {
            cal_box.style.left = findPosX(cal_link) + 17 + 'px';
        }
        else {
            // since style's width is in em, it'd be tough to calculate
            // px value of it. let's use an estimated px for now
            // TODO: IE returns wrong value for findPosX when in rtl mode
            //       (it returns as it was left aligned), needs to be fixed.
            cal_box.style.left = findPosX(cal_link) - 180 + 'px';
        }
        cal_box.style.top = findPosY(cal_link) - 75 + 'px';
    
        cal_box.style.display = 'block';
        addEvent(window, 'click', function() { DateTimeShortcuts.dismissCalendar(num); return true; });
    },
    dismissCalendar: function(num) {
        document.getElementById(DateTimeShortcuts.calendarDivName1+num).style.display = 'none';
    },
    drawPrev: function(num) {
        DateTimeShortcuts.calendars[num].drawPreviousMonth();
    },
    drawNext: function(num) {
        DateTimeShortcuts.calendars[num].drawNextMonth();
    },
    drawPrevY: function(num) {
        DateTimeShortcuts.calendars[num].drawPreviousYear();
    },
    drawNextY: function(num) {
        DateTimeShortcuts.calendars[num].drawNextYear();
    },
    handleCalendarCallback: function(num) {
        return "function(y, m, d) { DateTimeShortcuts.calendarInputs["+num+"].value = (d<10?'0':'')+d+'/'+(m<10?'0':'')+m+'/'+y; document.getElementById(DateTimeShortcuts.calendarDivName1+"+num+").style.display='none';}";
    },
    handleCalendarQuickLink: function(num, offset) {
	var date = new Date();
	date.setDate(date.getDate() + offset);
	y = date.getFullYear();
	m = date.getMonth()+1;
	d = date.getDate();
	DateTimeShortcuts.calendarInputs[num].value = (d<10?'0':'')+d+'/'+(m<10?'0':'')+m+'/'+y;
	DateTimeShortcuts.dismissCalendar(num);
    },
    cancelEventPropagation: function(e) {
        if (!e) e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    }
}

addEvent(window, 'load', DateTimeShortcuts.init);
