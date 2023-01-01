// Import hooks
import { useEffect, useState } from "react";

// Import bootstrap components
import { Form } from "react-bootstrap";

// Import styled components
import {
  StyledPreviewImage,
  ImageContainer,
  Image,
  LinkForm,
} from "./PreviewImage.styled";

/**
 * PreviewImage component to preview the selected image in create post image and videos tab
 *
 * @param {Number} selectedImageId - The id of the selected image
 * @param {Array} files - The array of images
 * @returns {React.Component} PreviewImage component
 */
const PreviewImage = ({ selectedImageId, files }) => {
  // State to store the selected image
  const [image, setImage] = useState(null);

  useEffect(() => {
    // Find the selected image
    if (selectedImageId) {
      // Find the selected image
      const selectedImage = files.find(
        (file) => file.name + file.uploadDate === selectedImageId
      );
      // Set the selected image to image state
      setImage(selectedImage);
    }
    if (files && files.length !== 0) setImage(files[0]);
    // Set the selected image to image state

    // Make sure to revoke the data uris to avoid memory leaks, will run on unmount
    return () => files.forEach((file) => URL.revokeObjectURL(file.preview));
  }, [selectedImageId, files, image]);
  return (
    <StyledPreviewImage>
      {image && (
        <>
          <ImageContainer>
            <Image
              as={image.type.toLowerCase().includes("video") ? "video" : "img"}
              src={image.src}
              controls={image.type.toLowerCase().includes("video")}
              alt="selected"
              id="preview-image"
              data-testid="image"
            />
          </ImageContainer>
        </>
      )}
    </StyledPreviewImage>
  );
};

export default PreviewImage;
