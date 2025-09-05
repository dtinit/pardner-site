(function() {
  const MODAL_TRIGGER_ATTRIBUTE_NAME = 'data-modal-trigger-for';
  const MODAL_PAGE_TRIGGER_ATTRIBUTE_NAME = 'data-modal-page-trigger-for';
  const MODAL_PAGE_CLASS_NAME = 'js-modal-page';
  const MODAL_CLOSE_TRIGGER_CLASS_NAME = 'js-close-modal';

  const triggerModal = (modalUrl) => {
    fetch(modalUrl)
      .then((response) => response.text())
      .then((modalContent) => {
        const modalEl = document.getElementById('modal');
        modalEl.innerHTML = modalContent;

        // Wire up close buttons
        modalEl.querySelectorAll(`.${MODAL_CLOSE_TRIGGER_CLASS_NAME}`).forEach((el) => {
          el.addEventListener('click', () => {
            modalBackdropEl.style.display = 'none';
          })
        });

        // Function for showing the current modal "page" only
        const showPage = (pageNum) => {
          const pageEls = modalEl.querySelectorAll(`.${MODAL_PAGE_CLASS_NAME}`);
          pageEls.forEach((pageEl, i) => {
            const displayStyle = i === (pageNum - 1) ? '' : 'none';
            pageEl.style.display = displayStyle;
          });
        }
            
        // Wire up elements that change the current modal page
        const pageTriggerEls = modalEl.querySelectorAll(`[${MODAL_PAGE_TRIGGER_ATTRIBUTE_NAME}]`);

        pageTriggerEls.forEach((pageTriggerEl) => {
          const pageNumberString = pageTriggerEl.getAttribute(MODAL_PAGE_TRIGGER_ATTRIBUTE_NAME);
          const parsedPageNumber = Number.parseInt(pageNumberString);
          if (Number.isNaN(parsedPageNumber)){
            console.error(new Error('Modal page trigger is not a number'));
            return;
          }
          pageTriggerEl.addEventListener('click', () => {
            showPage(parsedPageNumber);
          });
        });

        // Make sure only the first page is shown by default
        showPage(1);

        // Finally, reveal the modal
        const modalBackdropEl = document.getElementById('modal-backdrop');
        modalBackdropEl.style.display = '';
      })
  }

  const addModalTriggers = () => {
    const modalTriggers = document.querySelectorAll(
      `[${MODAL_TRIGGER_ATTRIBUTE_NAME}]`
    );
    modalTriggers.forEach((triggerEl) => {
      const modalUrl = triggerEl.getAttribute(MODAL_TRIGGER_ATTRIBUTE_NAME);
      triggerEl.addEventListener("click", () => {
        triggerModal(modalUrl);
      });
    });
    window.pardnersite = Object.assign({}, window.pardnersite, {
      triggerModal,
    });
  };

  // Need an observer for the home page study elements since these get
  // rendered after DOMContentLoaded gets fired.
  const observer = new MutationObserver((mutationList, observer) => {
    mutationList.forEach((mutation) => {
      if (mutation.type === "childList") {
        addModalTriggers();
      }
    });
  });

  const fetchAndRenderFilteredStudies = (serviceName) => {
    const path = serviceName
      ? `/study_list_items?filtered_service_name=${encodeURIComponent(
          serviceName
        )}`
      : '/study_list_items';
    fetch(path)
      .then((response) => response.text())
      .then((studyListItemsHTML) => {
        const studyListOuterElements =
          document.getElementsByClassName('study-list');
        for (const studyList of studyListOuterElements) {
          observer.observe(studyList, { childList: true });
          studyList.innerHTML = studyListItemsHTML;
        }
      });
  };

  document.addEventListener('DOMContentLoaded', () => {
    // original call to open modal when Data Donation button is clicked,
    // in the case when the single-study page is accessed.
    addModalTriggers();
    const selectHTMLElements = document.getElementsByClassName(
      'homepage--studies-list-header-dropdown'
    );
    if (selectHTMLElements.length > 0) {
      const selectHTMLElement = selectHTMLElements.item(0);
      // first time loading
      fetchAndRenderFilteredStudies(selectHTMLElement.value);
      // future changes
      selectHTMLElement.addEventListener('change', (event) =>
        fetchAndRenderFilteredStudies(event.target.value)
      );
    }
  });
})();
