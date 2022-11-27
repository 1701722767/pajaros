import { Uploader, Loader, Form, Button,Message,useToaster } from "rsuite";
import {URLContext} from '../contexts/url'

import React from "react";
import { FlexboxGrid } from "rsuite";
import ImageIcon from "@rsuite/icons/Image";

function previewFile(file, callback) {
  const reader = new FileReader();
  reader.onloadend = () => {
    callback(reader.result);
  };
  reader.readAsDataURL(file);
}

async function postData(url = "", formData = null) {
  const response = await fetch(url, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: formData,
  });
  return response.json();
}

const Predict = () => {
  const [uploading, setUploading] = React.useState(false);
  const [fileInfo, setFileInfo] = React.useState(null);
  const [fileList, setFileList] = React.useState([]);
  const [idImagen, setIdImagen] = React.useState("");
  const [response, setResponse] = React.useState({});
  const [error, setError] = React.useState("");
  const { url, setUrl } = React.useContext(URLContext);
  const toaster = useToaster();

  function doRequest(id, file) {
    if(!id){
      toaster.push(
        <Message showIcon type="error" closable>
          Debe ingresar un id para la imagen
        </Message>
      ,{value: 'topStart'});
      return
    }

    if(!file){
      toaster.push(
        <Message showIcon type="error" closable>
          Debe ingresar una imagen
        </Message>
      ,{value: 'topStart'});
      return
    }

    let formData = new FormData();
    formData.append("imagen", file);

    postData(`${url}?idImagen=${id}`,
      formData
    )
      .then((data) => {
        setResponse(data);
        setError("")
      })
      .catch((e) => {
        setError(e.message);
        setResponse({})
      });
  }

  return (
    <>
      <br />
      <Form justify="center" fluid>
        <h5 className="text-center">
          <b>Ingrese la imagen para la predicción</b>
        </h5>
        <br />
        <FlexboxGrid justify="center">
          <Uploader
            fileListVisible={false}
            listType="picture-text"
            disabledFileItem={true}
            action=""
            autoUpload={false}
            multiple={false}
            draggable={true}
            defaultFileList={fileList}
            onChange={(files) => {
              setUploading(true);
              setFileInfo(null);

              const file = files[files.length - 1];
              setFileList([file]);

              previewFile(file.blobFile, (value) => {
                setFileInfo(value);
                setUploading(false);
              });
            }}
          >
            <button style={{ width: 300, height: 300 }}>
              {uploading && <Loader backdrop center />}
              {fileInfo ? (
                <img src={fileInfo} width="100%" alt="Imagen pájaro" />
              ) : (
                <ImageIcon style={{ fontSize: 80 }} />
              )}
            </button>
          </Uploader>
        </FlexboxGrid>
        <br />
        <Form.Group controlId="idImagen">
          <Form.ControlLabel>
            <b>ID imagen</b>
          </Form.ControlLabel>
          <Form.Control
            value={idImagen}
            onChange={setIdImagen}
            name="url"
            placeholder="Ingresa el id de la imagen"
          />
        </Form.Group>
        <FlexboxGrid justify="center">
          <Button
            onClick={() => {
              doRequest(idImagen, fileInfo);
            }}
            className="width-100"
            size="lg"
            appearance="primary"
          >
            PREDECIR
          </Button>
        </FlexboxGrid>
      </Form>
      <br />
      <hr />
      <div>
        <b>Respuesta:</b>
        <br />
        Id Imagen: {response.idImagen} <br />
        Predicción: {response.prediccion} <br />
        Probabilidaes: <br />
        {response.probabilidades !== undefined &&
          response.probabilidades.map((probabilidad, index) => {
            return <p key={index}>{probabilidad}</p>;
          })}
        <br />
      </div>
      <hr />
      <p>
        <b>Error:</b>
        <br />
        <br /> {error !== "" && JSON.stringify(error)}
      </p>
      <br />
    </>
  );
};

export default Predict;
