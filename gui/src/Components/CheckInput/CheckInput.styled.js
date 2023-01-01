import styled from "styled-components";
import Modal from "react-bootstrap/Modal";
import Alert from "react-bootstrap/Alert";

export const ContentForm = styled.div`
  display: flex;
`;
export const ModalStyled = styled(Modal)`
  .btn-close:focus {
    box-shadow: none;
  }

  & .fade .modal-backdrop .show {
    background: rgb(28 28 28 / 90%);
  }

  & .btn-close :focus {
    box-shadow: none !important;
  }

  & .modal-content {
    color: ${({ theme }) => theme.color.primary};
    background-color: ${({ theme }) => theme.background.primary} !important;
    margin-top: 16%;
  }

  & .form-control:focus {
    box-shadow: none;
    border: 1px solid ${({ theme }) => theme.color.secondary} !important;
  }

  & .modal-content p {
    color: ${({ theme }) => theme.color.gray};
    margin-bottom: 30px;
    font-size: 12px;
    line-height: 16px;
    font-weight: 400;
  }

  & .modal-title {
    font-size: 16px;
    line-height: 20px;
    color: ${({ theme }) => theme.color.primary} !important;
    display: flex;
    -ms-flex-pack: justify;
    justify-content: space-between;
  }

  & .modal-footer {
    background-color: ${({ theme }) => theme.background.post_background};
  }
`;
export const AlarmInput = styled.p`
  color: ${({ alarmValue }) => (alarmValue > 0 ? true : "#ea0027")} !important;
`;

export const CheckFormContainer = styled.div`
  margin-bottom: 30px;
  h6 {
    margin-bottom: 20px !important;
  }
  display: flex;
  margin-left: 30px;
`;

export const Ico = styled.div`
  margin: 0 4px;
  align-self: baseline;
  color: #878a8c;
  svg {
    vertical-align: unset !important;
  }
`;

export const LabelForm = styled.label`
  display: flex;
  align-items: center;
`;

export const FormCheckContainer = styled.div`
  display: flex;
  margin-left: 16px;

  .form-check-input {
    width: 1.5em;
    height: 1.5em;
    margin-top: 0.2em !important;

    :checked {
      background-color: #0079d3;
    }

    :focus {
      box-shadow: none;
    }
  }
`;
export const FormInput = styled.input`
  width: 1em;
  height: 1em;

  :checked {
    background-color: #0079d3;
  }

  :focus {
    box-shadow: none;
  }
`;
export const FormCheckLabel = styled.label`
  font-size: 16px;
  line-height: 18px;
  font-weight: 500;
  display: flex;
  font-family: sans-serif;
  vertical-align: top;
  padding-left: 2px;
  margin-top: -1px;
  align-items: center;
`;
export const Content = styled.div`
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  color: ${({ theme }) => theme.color.muted};
  margin: 1px 0 0 4px;
`;
export const AdultCheck = styled.label`
  align-items: center;
  display: flex;

  .form-check-input {
    width: 1.3em;
    height: 1.3em;
    fill: #878a8c;

    :focus {
      box-shadow: none;
    }

    :checked {
      background-color: #0079d3;
    }
  }
`;
export const NSFW = styled.span`
  font-size: 12px;
  line-height: 17px;
  display: inline-block;
  background-color: #ff585b;
  font-weight: 500;
  border-radius: 2px;
  padding: 0 4px;
  color: ${({ theme }) => theme.background.primary} !important;
  margin: 0 4px 0 8px;
`;
export const Adult = styled.div`
  font-size: 16px;
  line-height: 20px;
  margin-bottom: 4px;
  font-weight: 500;
`;
export const CheckBoxInput = styled.input`
  width: 1.5em;
  height: 1.1em;
  fill: #878a8c;

  :focus {
    box-shadow: none;
  }

  :checked {
    background-color: #0079d3;
  }
`;
export const CloseBtn = styled.button`
  margin-left: 8px;
  font-family: Noto Sans, Arial, sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: unset;
  background-color: ${({ theme }) => theme.background.primary};
  line-height: 17px;
  text-transform: unset;
  min-height: 32px;
  min-width: 32px;
  padding: 4px 16px;
  border: 1px solid ${({ theme }) => theme.background.secondary};
  color: ${({ theme }) => theme.color.secondary};
  border-radius: 999px;

  :hover {
    background-color: ${({ theme }) => theme.background.hover_background};
  }
`;
export const CreateBtn = styled.button`
  background-color: ${({ theme }) => theme.color.secondary};
  position: relative;
  margin-left: 8px;
  color: ${({ theme }) => theme.background.primary};
  font-family: Noto Sans, Arial, sans-serif;
  font-size: 14px;
  font-weight: 700;
  border: none;
  border-radius: 999px;
  letter-spacing: unset;
  line-height: 17px;
  text-transform: unset;
  min-height: 32px;
  min-width: 32px;
  padding: 4px 16px;

  :hover {
    background-color: ${({ theme }) =>
      theme.background.hover_background_button_blue};
  }
`;
export const UsedCommunity = styled.div`
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  color: red;
  padding-top: 4px;
  text-align: right;
  display: flex;
  margin: -32px 0 16px;
  span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
`;
export const AlertSyled = styled(Alert)`
  width: 40%;
  margin: auto;
`;
export const BodyStyled = styled.div`
  margin-top: 7px;
`;
