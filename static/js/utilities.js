
function close_modal(dialog, e) {
    const dialogDimensions = dialog.getBoundingClientRect()
    //console.log(dialogDimensions)
    if (
      e.clientX < dialogDimensions.left ||
      e.clientX > dialogDimensions.right ||
      e.clientY < dialogDimensions.top ||
      e.clientY > dialogDimensions.bottom
    ) {
      dialog.close()
    }
  }
