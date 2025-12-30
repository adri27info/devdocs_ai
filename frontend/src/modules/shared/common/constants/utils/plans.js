import { CheckIcon, XMarkIcon, StarIcon } from '@heroicons/vue/24/outline';

export const PLANS = [
  {
    name: 'Free Plan',
    price: '$0',
    description: 'Perfect for solo developers just starting out',
    features: [
      { text: 'Up to 2 projects maximum', icon: CheckIcon, type: 'success' },
      { text: 'Only public projects', icon: CheckIcon, type: 'success' },
      { text: 'Export in plain text only', icon: CheckIcon, type: 'success' },
      { text: 'Documentation generation (only owner)', icon: CheckIcon, type: 'success' },
      { text: 'Private projects', icon: XMarkIcon, type: 'neutral' },
      { text: 'Rate documentation collaboration', icon: XMarkIcon, type: 'neutral' },
      { text: 'PDF export', icon: XMarkIcon, type: 'neutral' },
      { text: 'Up to 5 projects', icon: XMarkIcon, type: 'neutral' },
    ],
    btnText: 'Start free',
  },
  {
    name: 'Premium Plan',
    price: '$20',
    description: 'Ideal for small teams and professional projects',
    features: [
      { text: 'Up to 5 projects maximum', icon: CheckIcon, type: 'success' },
      { text: 'Public and private projects', icon: CheckIcon, type: 'success' },
      {
        text: 'Rate documentation collaboration (up to 2 members)',
        icon: CheckIcon,
        type: 'success',
      },
      { text: 'Export in plain text and PDF', icon: CheckIcon, type: 'success' },
      { text: 'Documentation generation (only owner)', icon: CheckIcon, type: 'success' },
    ],
    popular: true,
    badge: {
      icon: StarIcon,
      text: 'Most popular',
    },
    btnText: 'Upgrade to premium',
  },
];
