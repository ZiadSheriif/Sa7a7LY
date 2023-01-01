import React, { useState } from "react";
import {
  CheckFormContainer,
  FormCheckContainer,
  FormCheckLabel,
  Ico,
  LabelForm,
  ContentForm,
} from "./CheckInput.styled";

import {
  FcIntegratedWebcam,
  FcOldTimeCamera,
  FcCompactCamera,
  FcMms,
} from "react-icons/fc";

const CheckInput = ({ codesChoice,digitsChoice,setDigitChoice, setCodesChoice }) => {
  // const [currentCode, setCurrentCode] = useState("1");
  // const [numericalValue, setNumericalValue] = useState("1");

  return (
    <ContentForm>
      <CheckFormContainer>
        <FormCheckContainer>
          <input
            className="form-check-input"
            type="radio"
            name="radio-input-1"
            value="1"
            id="ocrID"
            onChange={(e) => setCodesChoice(e.target.value)}
            defaultChecked={codesChoice === "1"}
          />
          <LabelForm htmlFor="ocrID">
            <Ico>
              <FcCompactCamera size={22} />
            </Ico>
            <FormCheckLabel htmlFor="ocrID">OCR ID</FormCheckLabel>
          </LabelForm>
        </FormCheckContainer>
        <FormCheckContainer>
          <input
            className="form-check-input"
            type="radio"
            value="2"
            aria-label="classifierID"
            name="radio-input-1"
            id="classifierID"
            onChange={(e) => setCodesChoice(e.target.value)}
            defaultChecked={codesChoice === "2"}
          />
          <LabelForm htmlFor="classifierID">
            <Ico>
              <FcOldTimeCamera size={22} />
            </Ico>
            <FormCheckLabel htmlFor="classifierID">
              Classifier ID
            </FormCheckLabel>
          </LabelForm>
        </FormCheckContainer>
      </CheckFormContainer>

      <CheckFormContainer>
        <FormCheckContainer>
          <input
            className="form-check-input"
            type="radio"
            name="radio-input-2"
            value="1"
            id="ocrID"
            onChange={(e) => setDigitChoice(e.target.value)}
            defaultChecked={digitsChoice === "1"}
          />
          <LabelForm htmlFor="ocrID">
            <Ico>
              <FcIntegratedWebcam size={22} />
            </Ico>
            <FormCheckLabel htmlFor="ocrID">OCR</FormCheckLabel>
          </LabelForm>
        </FormCheckContainer>
        <FormCheckContainer>
          <input
            className="form-check-input"
            type="radio"
            value="2"
            aria-label="classifierID"
            name="radio-input-2"
            id="classifierID"
            onChange={(e) => setDigitChoice(e.target.value)}
            defaultChecked={digitsChoice === "2"}
          />
          <LabelForm htmlFor="classifierID">
            <Ico>
              <FcMms size={22} />
            </Ico>
            <FormCheckLabel htmlFor="classifierID">Classifier</FormCheckLabel>
          </LabelForm>
        </FormCheckContainer>
      </CheckFormContainer>
    </ContentForm>
  );
};
export default CheckInput;
