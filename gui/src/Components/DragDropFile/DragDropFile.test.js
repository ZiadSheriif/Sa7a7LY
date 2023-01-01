import { mount, shallow } from "enzyme";
import React from "react";

// Import components
import DragAndDropFile from "./DragDropFile";

describe("Drag and drop file", () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<DragAndDropFile files={[]} setFiles={() => "test"} />);
  });

  it("should render without crashing", () => {
    expect(wrapper).toMatchSnapshot();
  });
});
