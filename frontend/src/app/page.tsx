import { Button } from '@/components/ui/button';

export default function TestPage() {
  return (
    <div className='flex flex-col items-center justify-center min-h-screen gap-4'>
      <h1 className='text-2xl font-bold'>Shadcn Installation Test</h1>

      <div className='p-6 border rounded-lg shadow-sm bg-card'>
        <p className='mb-4 text-muted-foreground'>
          If you see a styled button below, shadcn is working!
        </p>

        <div className='flex gap-2'>
          {/* Test the Primary Variant */}
          <Button>Default Button</Button>

          {/* Test the Outline Variant (checks border colors) */}
          <Button variant='outline'>Outline</Button>

          {/* Test the Destructive Variant (checks red theme variables) */}
          <Button variant='destructive'>Destructive</Button>
        </div>
        <div className='h-20 w-20 bg-orange-500 text-white flex items-center justify-center rounded-full shadow-xl animate-bounce'>
          V4 TEST
        </div>
      </div>
    </div>
  );
}
