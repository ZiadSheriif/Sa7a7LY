// Import styled components
import {
  DeleteButton,
  StyledUploadedImage,
  Thumb,
  ThumbInner,
} from "./UploadedImage.styled";

// Import icons
import { ImCross } from "react-icons/im";

// Import hooks
import React, { useEffect } from "react";

/**
 * Uploaded image component in images & videos tab
 *
 * @param {File} file - The uploaded image
 * @param {Function} deleteFile - The function to delete the image
 * @param {Boolean} isSelected - Boolean to check if the image is selected
 * @param {Number} selectedImageId - The id of the selected image
 * @param {Number} id - The id of this image
 * @param {Function} handleClick - The function to handle the click event on image
 * @returns {React.Component} - Uploaded image component in images & videos tab
 */
const UploadedImage = ({
  file,
  deleteFile,
  isSelected,
  selectedImageId,
  id,
  handleClick,
}) => {
  useEffect(() => {
    // When image first render mark it as selected
    handleClick(id);
  }, []);
  return (
    <Thumb onClick={() => handleClick(id)}>
      <ThumbInner>
        <StyledUploadedImage
          className="uploaded-image"
          thumbnail={isSelected && selectedImageId === id}
          selected={isSelected && selectedImageId === id}
          as={file.type.toLowerCase().includes("video") ? "video" : "img"}
          src={file.src}
          // Revoke data uri after image is loaded
          onLoad={() => {
            URL.revokeObjectURL(file.preview);
          }}
          alt="uploaded preview"
        />
        <DeleteButton
          data-testid="delete-button"
          className="delete-img-danger"
          variant="danger"
          onClick={() => deleteFile(file)}
        >
          <ImCross size={20} />
        </DeleteButton>
      </ThumbInner>
    </Thumb>
  );
};

export default UploadedImage;
