export class MissingCoreParamError extends Error {
  constructor(message = 'Param is required') {
    super(message);
    this.name = 'MissingCoreParamError';
  }
}
