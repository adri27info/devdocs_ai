import { CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/outline';

class ToasterHelperClass {
  constructor() {
    this.position = {
      'top-right': 'top-2 right-0 sm:right-3',
    };

    this.icons = {
      success: CheckCircleIcon,
      error: XCircleIcon,
    };

    this.iconColors = {
      success: 'text-green-700',
      error: 'text-red-700',
    };

    this.bgColors = {
      success: 'bg-green-700',
      error: 'bg-red-700',
    };

    this.borderColors = {
      success: 'border-green-700',
      error: 'border-red-700',
    };

    this.textColors = {
      success: 'text-green-700',
      error: 'text-red-700',
    };
  }

  getToastConfig() {
    return {
      position: this.position,
      icons: this.icons,
      iconColors: this.iconColors,
      bgColors: this.bgColors,
      borderColors: this.borderColors,
      textColors: this.textColors,
    };
  }
}

export const ToasterHelper = new ToasterHelperClass();
