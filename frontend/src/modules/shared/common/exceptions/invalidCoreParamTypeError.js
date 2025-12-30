export class InvalidCoreParamTypeError extends Error {
  constructor(message = 'Param must be a string') {
    super(message);
    this.name = 'InvalidCoreParamTypeError';
  }
}
