export function useRequestSendData(axiosInstance, getHeaders) {
  function sendData(url, fields, method = 'post') {
    const config = {
      headers: fields.attachment ? getHeaders('form') : getHeaders('json'),
    };

    let data = fields;

    if (fields.attachment) {
      const formData = new FormData();

      Object.entries(fields).forEach(([key, value]) => {
        formData.append(key, value);
      });

      data = formData;
    }

    return axiosInstance[method.toLowerCase()](url, data, config);
  }

  return { sendData };
}
