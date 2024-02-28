(function ($) {
    'use strict';

jQuery(document).ready(function () {
  const dismissablePanels = document.querySelectorAll('.dismissable-panel');
		
   dismissablePanels.forEach(panel => {
      const closeButton = panel.querySelector('.dismiss-button');
      closeButton.addEventListener('click', () => {
        panel.style.display = 'none';
      });
    });


});
})(jQuery);
