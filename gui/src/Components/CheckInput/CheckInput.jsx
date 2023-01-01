import {
  CheckFormContainer,
  FormCheckContainer,
  FormCheckLabel,
  Ico,
  LabelForm,
  ContentForm,
  AlertSyled,
  BodyStyled,
} from "./CheckInput.styled";

import {
  FcOldTimeCamera,
  FcCompactCamera,
  FcMms,
  FcPicture,
} from "react-icons/fc";

const CheckInput = ({
  codesChoice,
  digitsChoice,
  setDigitChoice,
  setCodesChoice,
}) => {
  return (
    <>
      <ContentForm>
        <BodyStyled>
          <CheckFormContainer>
            <FormCheckContainer>
              <input
                className="form-check-input"
                type="radio"
                name="radio-input-1"
                value="1"
                id="ocrID-1"
                onChange={(e) => setCodesChoice(e.target.value)}
                defaultChecked={codesChoice === "1"}
              />
              <LabelForm htmlFor="ocrID-1">
                <Ico>
                  <FcCompactCamera size={30} />
                </Ico>
                <FormCheckLabel htmlFor="ocrID-1">
                  Student ID OCR
                </FormCheckLabel>
              </LabelForm>
            </FormCheckContainer>
            <FormCheckContainer>
              <input
                className="form-check-input"
                type="radio"
                value="2"
                aria-label="classifierID"
                name="radio-input-1"
                id="classifierID-1"
                onChange={(e) => setCodesChoice(e.target.value)}
                defaultChecked={codesChoice === "2"}
              />
              <LabelForm htmlFor="classifierID-1">
                <Ico>
                  <FcOldTimeCamera size={30} />
                </Ico>
                <FormCheckLabel htmlFor="classifierID-1">
                  Student ID Classifier
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
                id="ocrID-2"
                onChange={(e) => setDigitChoice(e.target.value)}
                defaultChecked={digitsChoice === "1"}
              />
              <LabelForm htmlFor="ocrID-2">
                <Ico>
                  <FcPicture size={30} />
                </Ico>
                <FormCheckLabel htmlFor="ocrID-2">Numbers OCR</FormCheckLabel>
              </LabelForm>
            </FormCheckContainer>
            <FormCheckContainer>
              <input
                className="form-check-input"
                type="radio"
                value="2"
                aria-label="classifierID"
                name="radio-input-2"
                id="classifierID-2"
                onChange={(e) => setDigitChoice(e.target.value)}
                defaultChecked={digitsChoice === "2"}
              />
              <LabelForm htmlFor="classifierID-2">
                <Ico>
                  <FcMms size={30} />
                </Ico>
                <FormCheckLabel htmlFor="classifierID-2">
                  Numbers Classifier
                </FormCheckLabel>
              </LabelForm>
            </FormCheckContainer>
          </CheckFormContainer>
        </BodyStyled>
      </ContentForm>

      {/* <AlertSyled variant={"success"}>
        DONE! Output written to 'autoFiller.xls'
      </AlertSyled> */}
    </>
  );
};
export default CheckInput;
