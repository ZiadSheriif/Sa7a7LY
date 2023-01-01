// Import components
import DragAndDropFile from "../DragDropFile/DragDropFile";

// Import styled components
import {
  PostButton,
  StyledImageAndVideoFrom,
  CancelButton,
  SubmitButtons,
} from "./ImageAndVideoForm.styled";

// Import hooks
import { useState, useRef } from "react";

// Import hooks
import { useEffect } from "react";
import { Spinner } from "react-bootstrap";

/**
 * Image and video form component (The form that appears when you click on the image and video tab in main section)
 * @param {Function} submitPost - Function to submit the post
 * @returns {React.Component} - Image and video form component (The form that appears when you click on the image and video tab in main section)
 */
const ImageAndVideoForm = ({ submitPost, isLoadingSubmit }) => {
  // State for flair modal
  const [modalShow, setModalShow] = useState(false);

  // State for flair
  const [flairIndex, setFlairIndex] = useState(null);

  const [files, setFiles] = useState([]);

  return (
    <>
      <StyledImageAndVideoFrom>
        <DragAndDropFile files={files} setFiles={setFiles} />
        <SubmitButtons>
          <CancelButton variant="light">Cancel</CancelButton>
          <PostButton id="post">
            {!isLoadingSubmit && "Post"}
            {isLoadingSubmit && <Spinner animation="border" variant="light" />}
          </PostButton>
        </SubmitButtons>
      </StyledImageAndVideoFrom>
    </>
  );
};

export default ImageAndVideoForm;
