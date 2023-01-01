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
  FcMms
} from "react-icons/fc";

const CheckInput = () => {
  const [currentCode, setCurrentCode] = useState("ocrID");
  const [numericalValue, setNumericalValue] = useState("ocrID");

  return (
    <ContentForm>
      <CheckFormContainer>
        <FormCheckContainer>
          <input
            className="form-check-input"
            type="radio"
            name="radio-input-1"
            value="ocrID"
            id="ocrID"
            onChange={(e) => setCurrentCode(e.target.value)}
            defaultChecked={currentCode === "ocrID"}
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
            value="classifierID"
            aria-label="classifierID"
            name="radio-input-1"
            id="classifierID"
            onChange={(e) => setCurrentCode(e.target.value)}
            defaultChecked={currentCode === "classifierID"}
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
            value="ocrID"
            id="ocrID"
            onChange={(e) => setNumericalValue(e.target.value)}
            defaultChecked={numericalValue === "ocrID"}
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
            value="classifierID"
            aria-label="classifierID"
            name="radio-input-2"
            id="classifierID"
            onChange={(e) => setNumericalValue(e.target.value)}
            defaultChecked={numericalValue === "classifierID"}
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
