const handleResize = () => {
    // Update the canvas size based on the screen size
    const screenWidth = window.innerWidth;
    if (screenWidth <= 576) {
      // Small screens
      Canvas.width = props.imageMetadata.width * 0.5;
      Canvas.height = props.imageMetadata.height * 0.5;
    } else if (screenWidth <= 992) {
      // Medium screens
      Canvas.width = props.imageMetadata.width * 0.75;
      Canvas.height = props.imageMetadata.height * 0.75;
    } else {
      // Large screens
      Canvas.width = props.imageMetadata.width * 0.90;
      Canvas.height = props.imageMetadata.height * 0.90;
    }

  };
