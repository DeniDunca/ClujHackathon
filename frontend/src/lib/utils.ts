import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format a date string or Date object to a readable format
 * @param dateInput - Date string (ISO format) or Date object
 * @param format - Optional format string. Default: 'dd:mm:yyyy HH:MM'
 *                 Available tokens:
 *                 - dd: day with leading zero
 *                 - mm: month with leading zero
 *                 - yyyy: full year
 *                 - HH: hours (24h format) with leading zero
 *                 - MM: minutes with leading zero
 *                 - ss: seconds with leading zero
 * @returns Formatted date string
 *
 * @example
 * // Default format (dd:mm:yyyy HH:MM)
 * getUploadDate('2024-01-15T14:30:45Z') // Returns: "15:01:2024 14:30"
 *
 * // Custom formats
 * getUploadDate('2024-01-15T14:30:45Z', 'dd/mm/yyyy') // Returns: "15/01/2024"
 * getUploadDate('2024-01-15T14:30:45Z', 'yyyy-mm-dd HH:MM:ss') // Returns: "2024-01-15 14:30:45"
 * getUploadDate(new Date(), 'dd.mm.yyyy HH:MM') // Returns: "15.01.2024 14:30"
 */
export function getUploadDate(dateInput: string | Date, format: string = 'dd:mm:yyyy HH:MM'): string {
  try {
    const date = typeof dateInput === 'string' ? new Date(dateInput) : dateInput

    // Check if date is valid
    if (isNaN(date.getTime())) {
      return 'Invalid date'
    }

    // Helper function to pad numbers with leading zero
    const pad = (num: number): string => num.toString().padStart(2, '0')

    // Extract date components
    const day = pad(date.getDate())
    const month = pad(date.getMonth() + 1) // getMonth() returns 0-11
    const year = date.getFullYear().toString()
    const hours = pad(date.getHours())
    const minutes = pad(date.getMinutes())
    const seconds = pad(date.getSeconds())

    // Replace format tokens with actual values
    return format
      .replace(/dd/g, day)
      .replace(/mm/g, month)
      .replace(/yyyy/g, year)
      .replace(/HH/g, hours)
      .replace(/MM/g, minutes)
      .replace(/ss/g, seconds)
  } catch (error) {
    console.error('Error formatting date:', error)
    return 'Invalid date'
  }
}
