// Import components
import DragAndDropFile from "../DragDropFile/DragDropFile";
import CheckInput from "../CheckInput/CheckInput";
import Header from "../Header/Header";

// Import styled components
import {
  PostButton,
  StyledImageAndVideoFrom,
  CancelButton,
  SubmitButtons,
  HeadStyled,
} from "./ImageAndVideoForm.styled";

// Import hooks
import { useState, useRef } from "react";

// Import hooks
import { Spinner } from "react-bootstrap";

/**
 * Image and video form component (The form that appears when you click on the image and video tab in main section)
 * @param {Function} submitPost - Function to submit the post
 * @returns {React.Component} - Image and video form component (The form that appears when you click on the image and video tab in main section)
 */
const ImageAndVideoForm = ({ submitPost, isLoadingSubmit }) => {
  const [files, setFiles] = useState([]);
  const [codesChoice, setCodesChoice] = useState("1");
  const [digitsChoice, setDigitChoice] = useState("1");

  /**
   * Handle form submit
   */
  const submitForm = () => {
    submitPost({ attachments: files, codesChoice, digitsChoice });
  };
  return (
    <>
      <Header />
      <StyledImageAndVideoFrom>
        <DragAndDropFile files={files} setFiles={setFiles} oneFile={true} />
        <div>
          <HeadStyled>Auto-Filler</HeadStyled>
        </div>
        <SubmitButtons>
          <CancelButton variant="light">Cancel</CancelButton>
          <PostButton id="post" onClick={submitForm}>
            {!isLoadingSubmit && "Submit"}
            {isLoadingSubmit && <Spinner animation="border" variant="light" />}
          </PostButton>
        </SubmitButtons>
        <CheckInput
          codesChoice={codesChoice}
          digitsChoice={digitsChoice}
          setCodesChoice={setCodesChoice}
          setDigitChoice={setDigitChoice}
        />
      </StyledImageAndVideoFrom>
    </>
  );
};

export default ImageAndVideoForm;
