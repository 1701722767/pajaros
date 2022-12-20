import { Form } from "rsuite";
import { URLContext } from "../contexts/url";
import React from "react";
import { Notification } from "rsuite";

const Message = React.forwardRef(({ type, title, content, ...rest }, ref) => {
  return (
    <Notification
      className="width-100"
      ref={ref}
      {...rest}
      type={type}
      header={title}
    >
      {content}
    </Notification>
  );
});

const Settings = () => {
  const { url, setUrl } = React.useContext(URLContext);
  const changeHandler = value => {setUrl(value);console.log(url)};


  return (
    <>
      <br />
      <br />
      <Form fluid>
        <Form.Group controlId="url">
          <Form.ControlLabel>
            <b>URL</b>
          </Form.ControlLabel>
            <Form.Control
              value={url}
              onChange={changeHandler}
              name="url"
              placeholder="Ingresa una url para hacer la predicción"
            />

        </Form.Group>
      </Form>

      <hr />
      <Message
        type="info"
        title="Información"
        content="Acá pordrás insertar la URL a donde quieres que se hagan las peticiones para predecir el tipo de deporte."
      />
    </>
  );
};

export default Settings;
